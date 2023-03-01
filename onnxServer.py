import copy

import cv2
import onnxruntime
import numpy as np
# from retinaface.commons import preprocess, postprocess
import tensorflow as tf
import postprocess
import preprocess
from deepface.commons import functions
from keras.engine import data_adapter
from deepface.DeepFace import represent
import onnx
import matplotlib.pyplot as plt





# use model_simp as a standard ONNX model object

def run_onnx_detect_faces(img_, threshold=0.9):
    # 创建一个InferenceSession的实例，并将模型的地址传递给该实例
    global detectSess
    if 'detectSess' not in globals():
        detectSess = onnxruntime.InferenceSession('../models/retinaface.onnx')
    # 获取模型原始输入的字段名称
    input_name = detectSess.get_inputs()[0].name
    output_name = []
    for node in detectSess.get_outputs():
        output_name.append(node.name)
    # output_name = sess.get_outputs()[0].name
    # 加载图片
    img = copy.deepcopy(img_)
    # img = cv2.resize(img, (112, 112))
    # img = img.astype(np.float32)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    nms_threshold = 0.4
    decay4 = 0.5

    _feat_stride_fpn = [32, 16, 8]

    _anchors_fpn = {
        'stride32': np.array([[-248., -248., 263., 263.], [-120., -120., 135., 135.]], dtype=np.float32),
        'stride16': np.array([[-56., -56., 71., 71.], [-24., -24., 39., 39.]], dtype=np.float32),
        'stride8': np.array([[-8., -8., 23., 23.], [0., 0., 15., 15.]], dtype=np.float32)
    }

    _num_anchors = {'stride32': 2, 'stride16': 2, 'stride8': 2}

    proposals_list = []
    scores_list = []
    landmarks_list = []
    im_tensor, im_info, im_scale = preprocess.preprocess_image(img, True)
    # print(im_tensor)
    # print(im_tensor.shape)
    # 调用实例sess的run方法进行推理
    net_out = detectSess.run(output_name, {input_name: im_tensor})

    net_out = [elt for elt in net_out]
    sym_idx = 0
    # print(net_out)

    for _idx, s in enumerate(_feat_stride_fpn):
        _key = 'stride%s' % s
        scores = net_out[sym_idx]
        scores = scores[:, :, :, _num_anchors['stride%s' % s]:]

        bbox_deltas = net_out[sym_idx + 1]
        height, width = bbox_deltas.shape[1], bbox_deltas.shape[2]

        A = _num_anchors['stride%s' % s]
        K = height * width
        anchors_fpn = _anchors_fpn['stride%s' % s]
        anchors = postprocess.anchors_plane(height, width, s, anchors_fpn)
        anchors = anchors.reshape((K * A, 4))
        scores = scores.reshape((-1, 1))

        bbox_stds = [1.0, 1.0, 1.0, 1.0]
        bbox_deltas = bbox_deltas
        bbox_pred_len = bbox_deltas.shape[3] // A
        bbox_deltas = bbox_deltas.reshape((-1, bbox_pred_len))
        bbox_deltas[:, 0::4] = bbox_deltas[:, 0::4] * bbox_stds[0]
        bbox_deltas[:, 1::4] = bbox_deltas[:, 1::4] * bbox_stds[1]
        bbox_deltas[:, 2::4] = bbox_deltas[:, 2::4] * bbox_stds[2]
        bbox_deltas[:, 3::4] = bbox_deltas[:, 3::4] * bbox_stds[3]
        proposals = postprocess.bbox_pred(anchors, bbox_deltas)

        proposals = postprocess.clip_boxes(proposals, im_info[:2])

        if s == 4 and decay4 < 1.0:
            scores *= decay4

        scores_ravel = scores.ravel()
        order = np.where(scores_ravel >= threshold)[0]
        proposals = proposals[order, :]
        scores = scores[order]

        proposals[:, 0:4] /= im_scale
        proposals_list.append(proposals)
        scores_list.append(scores)

        landmark_deltas = net_out[sym_idx + 2]
        landmark_pred_len = landmark_deltas.shape[3] // A
        landmark_deltas = landmark_deltas.reshape((-1, 5, landmark_pred_len // 5))
        landmarks = postprocess.landmark_pred(anchors, landmark_deltas)
        landmarks = landmarks[order, :]

        landmarks[:, :, 0:2] /= im_scale
        landmarks_list.append(landmarks)
        sym_idx += 3

    proposals = np.vstack(proposals_list)
    if proposals.shape[0] == 0:
        landmarks = np.zeros((0, 5, 2))
        return np.zeros((0, 5)), landmarks
    scores = np.vstack(scores_list)
    scores_ravel = scores.ravel()
    order = scores_ravel.argsort()[::-1]

    proposals = proposals[order, :]
    scores = scores[order]
    landmarks = np.vstack(landmarks_list)
    landmarks = landmarks[order].astype(np.float32, copy=False)

    pre_det = np.hstack((proposals[:, 0:4], scores)).astype(np.float32, copy=False)

    # nms = cpu_nms_wrapper(nms_threshold)
    # keep = nms(pre_det)
    keep = postprocess.cpu_nms(pre_det, nms_threshold)

    det = np.hstack((pre_det, proposals[:, 4:]))
    det = det[keep, :]
    landmarks = landmarks[keep]

    resp = {}
    for idx, face in enumerate(det):
        label = 'face_' + str(idx + 1)
        resp[label] = {}
        resp[label]["score"] = face[4]

        resp[label]["facial_area"] = list(face[0:4].astype(int))

        resp[label]["landmarks"] = {}
        resp[label]["landmarks"]["right_eye"] = list(landmarks[idx][0])
        resp[label]["landmarks"]["left_eye"] = list(landmarks[idx][1])
        resp[label]["landmarks"]["nose"] = list(landmarks[idx][2])
        resp[label]["landmarks"]["mouth_right"] = list(landmarks[idx][3])
        resp[label]["landmarks"]["mouth_left"] = list(landmarks[idx][4])

    return resp


def run_onnx_extract_faces(img_, threshold=0.9, model=None, align=True, allow_upscaling=True):
    resp = []
    obj = run_onnx_detect_faces(img_=img_, threshold=threshold)

    img = copy.deepcopy(img_)

    if type(obj) == dict:
        for key in obj:
            identity = obj[key]

            facial_area = identity["facial_area"]
            facial_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]

            if align == True:
                landmarks = identity["landmarks"]
                left_eye = landmarks["left_eye"]
                right_eye = landmarks["right_eye"]
                nose = landmarks["nose"]
                mouth_right = landmarks["mouth_right"]
                mouth_left = landmarks["mouth_left"]

                facial_img = postprocess.alignment_procedure(facial_img, right_eye, left_eye, nose)

            resp.append(facial_img[:, :, ::-1])
    # elif type(obj) == tuple:

    return resp


def run_onnx_presentation(img):
    # 创建一个InferenceSession的实例，并将模型的地址传递给该实例
    global presentSess
    if 'presentSess' not in globals():
        presentSess = onnxruntime.InferenceSession('../models/facenet512.onnx')
    # 获取模型原始输入的字段名称
    input_name = presentSess.get_inputs()[0].name
    output_name = presentSess.get_outputs()[0].name

    input_shape_x, input_shape_y = 160, 160

    img = functions.preprocess_face(img=img
                                    , target_size=(input_shape_y, input_shape_x)
                                    , enforce_detection=False
                                    , detector_backend='opencv'
                                    , align=True)

    img = functions.normalize_input(img=img, normalization="base")

    # img = cv2.imread(img_path)
    # img = cv2.resize(img, (160, 160))
    # img = np.array(img).astype("float32")
    # print(img.shape)
    # 调用实例sess的run方法进行推理
    net_out = presentSess.run([output_name], {input_name: img})[0].tolist()[0]

    return net_out


def reprojectLandmark(landmark, w, h, x_, y_):
    landmark_ = np.asarray(np.zeros(landmark.shape))
    for i, point in enumerate(landmark):
        x = point[0] * w + x_
        y = point[1] * h + y_
        landmark_[i] = (x, y)
    return landmark_


def run_face_landmark(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_mean = np.array([127, 127, 127])
    img = (img - image_mean) / 128

    height, width, _ = img.shape
    x1 = 0
    y1 = 0
    x2 = width
    y2 = height
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    size = int(max([w, h]) * 1.1)
    cx = x1 + w // 2
    cy = y1 + h // 2
    x1 = cx - size // 2
    x2 = x1 + size
    y1 = cy - size // 2
    y2 = y1 + size
    dx = max(0, -x1)
    dy = max(0, -y1)
    x1 = max(0, x1)
    y1 = max(0, y1)

    edx = max(0, x2 - width)
    edy = max(0, y2 - height)
    x2 = min(width, x2)
    y2 = min(height, y2)

    sess = onnxruntime.InferenceSession('./models/pfld.onnx')

    # 获取模型原始输入的字段名称
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name

    input_shape_x, input_shape_y = 112, 112

    img = cv2.resize(img, (input_shape_x, input_shape_y))
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    img = img.astype("float32")

    net_out = sess.run([output_name], {input_name: img})[0].tolist()[0]
    landmark = np.array(net_out).reshape(-1, 2)
    # x1, x2 = 7, 225
    # y1, y2 = 68, 286
    # landmark = reprojectLandmark(landmark, x2 - x1, y2 - y1, x1, y1)

    x = []
    y = []
    for i, j in landmark:
        x.append(i)
        y.append(j)

    print(np.linalg.norm(([x[37], y[37]], [x[41], y[41]])))
    plt.scatter(x, y)
    plt.axis('off')
    plt.show()
    return