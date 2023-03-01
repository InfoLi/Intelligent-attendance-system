import copy
import math
import random
from sklearn.metrics import roc_curve
import cv2
import numpy as np
from retinaface import RetinaFace
import matplotlib.pyplot as plt
from deepface.DeepFace import represent
from deepface.commons import distance as dst
import os
from tools.enhanceTool import polyblurImg
from sklearn.datasets import fetch_lfw_pairs
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from deepface.commons import functions
from deepface.basemodels.Facenet import InceptionResNetV2


def rep(img):
    global FaceNetmodel
    if 'FaceNetmodel' not in globals():
        FaceNetmodel = InceptionResNetV2(128)
        FaceNetmodel.load_weights("./models/facenet_keras_weights.h5")

    input_shape_x, input_shape_y = 160, 160
    img = functions.preprocess_face(img=img
                                    , target_size=(input_shape_y, input_shape_x)
                                    , enforce_detection=False
                                    , detector_backend='retinaface'
                                    , align=True)

    img = functions.normalize_input(img=img, normalization='base')
    embedding = FaceNetmodel.predict(img)[0].tolist()

    return embedding


def detect(img_path, threshold=0.9):
    # img = cv2.imread(img_path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # resp = RetinaFace.detect_faces(img_path)
    # plt.imshow(img)
    # for face in resp:
    #     face_Matric = resp[face]["facial_area"]
    #     p1 = [face_Matric[1], face_Matric[0]]
    #     p2 = [face_Matric[1], face_Matric[2]]
    #     p3 = [face_Matric[3], face_Matric[0]]
    #     p4 = [face_Matric[3], face_Matric[2]]
    #     plt.plot([p1[1], p2[1]], [p1[0], p2[0]], color="yellow")
    #     plt.plot([p1[1], p3[1]], [p1[0], p3[0]], color="yellow")
    #     plt.plot([p2[1], p4[1]], [p2[0], p4[0]], color="yellow")
    #     plt.plot([p4[1], p3[1]], [p4[0], p3[0]], color="yellow")
    # plt.show()
    return RetinaFace.detect_faces(img_path=img_path, threshold=threshold)


def verify(img_path1, img_path2, threshold=0.4):
    img1 = RetinaFace.extract_faces(img_path1)
    img2 = RetinaFace.extract_faces(img_path2)

    if len(img1) != 1 and len(img2) != 1:
        print("无法监测到合适人像，可能是人像过多或是无法监测到人像")
        return False

    img1 = img1[0]
    img2 = img2[0]

    # plt.figure()
    # plt.imshow(img1)
    # plt.figure()
    # plt.imshow(img2)
    # plt.show()

    img1_representation = represent(img1, model_name="Facenet512", enforce_detection=False)
    img2_representation = represent(img2, model_name="Facenet512", enforce_detection=False)

    # print(img1_representation)
    # print(img2_representation)

    distance = dst.findCosineDistance(img1_representation, img2_representation)

    distance = np.float64(distance)

    if distance <= threshold:
        return 1
    else:
        return 0


def verify_imgs(img1, img2, threshold=0.4):
    img1 = RetinaFace.extract_faces(img1)[0]
    img2 = RetinaFace.extract_faces(img2)[0]
    # Facenet512
    img1_representation = represent(img1, model_name="Facenet512", enforce_detection=False)
    img2_representation = represent(img2, model_name="Facenet512", enforce_detection=False)
    distance = dst.findCosineDistance(img1_representation, img2_representation)
    distance = np.float64(distance)
    if distance <= threshold:
        return True
    else:
        return False


def evalutionByPhotos(photo_dir, threshold=0.4):
    adds = []
    # 获取每张图片的地址
    for addr in os.listdir(photo_dir):
        abosult_path = os.path.join(photo_dir, addr)
        adds.append(abosult_path)

    print("*" * 20 + "特征向量计算开始" + "*" * 20)
    img_representation = []
    for i in range(len(adds)):
        img = RetinaFace.extract_faces(adds[i])
        if len(img) != 1:
            continue
        # 获取特征向量
        img_representation.append(represent(img[0], model_name="VGG-Face", enforce_detection=False))

    print("*" * 20 + "准确率评估" + "*" * 20)
    rights = 0
    falses = 0
    # 评估特征向量的表示
    for i in range(len(img_representation)):
        for j in range(i + 1, len(img_representation)):
            distance = dst.findCosineDistance(img_representation[i], img_representation[j])
            distance = np.float64(distance)
            if distance <= threshold:
                rights += 1
            else:
                falses += 1

        print(f"中间准确率评估={rights / (rights + falses)}")

    print(f"整体准确率={rights / (rights + falses)}")


# 0.9651228733459357
# 0.9887523629489603 FaceNet512
def evalutionByLWF(dir_dir=r"E:\pythonProject\data\lfw", threshold=0.4):
    # dir_adds = []
    # # 获取每张图片的地址
    # for addr in os.listdir(dir_dir):
    #     # abosult_path = os.path.join(dir_dir, addr)
    #     dir_adds.append(addr)
    #
    # adds = {}
    # total = 0
    # for dir in dir_adds:
    #     # if len(os.listdir(os.path.join(dir_dir, dir))) <= 1:
    #     #     continue
    #     adds[dir] = []
    #     total += len(os.listdir(os.path.join(dir_dir, dir)))
    #     for img_path in os.listdir(os.path.join(dir_dir, dir)):
    #         adds[dir].append(os.path.join(dir_dir, dir, img_path))
    #
    # print("*" * 20 + "特征向量计算开始" + "*" * 20)
    # img_representation = {}
    # schedule = 1 / 100
    # now = 0
    # for key in adds:
    #     img_representation[key] = []
    #     for img_path in adds[key]:
    #         now += 1
    #         img = RetinaFace.extract_faces(img_path)
    #         if len(img) != 1:
    #             continue
    #         # 获取特征向量
    #         img_representation[key].append(represent(img[0], model_name="Facenet512", enforce_detection=False))
    #     if now / total >= schedule:
    #         print(f"当前进度为={now / total}")
    #         schedule += 1 / 100
    # np.save("./npy/lwf特征向量FaceNet512.npy", img_representation)
    img_representation = np.load("./npy/lwfFaceNet512.npy", allow_pickle=True).item()
    # 每个人的脸进行特征向量的表示
    averagePresentation = {}
    for key in img_representation:
        if img_representation[key] == []:
            continue
        t = img_representation[key]
        # 均值作为结果
        averageT = np.sum(t, 0) / len(t)
        averagePresentation[key] = averageT

    rights = 0
    falses = 0
    # 这里将对averagePresentation进行重构
    average_name = []
    average_value = []
    for key in averagePresentation:
        average_name.append(key)
        average_value.append(averagePresentation[key])
    average_value = np.array(average_value)

    distanceB = np.sqrt(np.sum(average_value * average_value, 1))
    for key in img_representation:
        t = img_representation[key]
        for i in range(len(t)):
            npT = np.array(t[i])
            similar = np.dot(average_value, npT) / (
                    np.sqrt(np.sum(np.multiply(npT, npT))) * distanceB)
            # print(similar)
            position = np.where(similar == np.max(similar))
            if average_name[position[0][0]] == key and (1 - np.max(similar)) < 0.58:
                rights += 1
            else:
                falses += 1
        print(f"中间准确率评估={rights / (rights + falses)}")

    print(f"整体准确率={rights / (rights + falses)}")


# =0.8970662941325883FaceNet512
def evalutionAgeDB(threshold=0.4):
    # dir = "./data/AgeDB"
    # imgs = {}
    # total = len(os.listdir(dir))
    # for img_name in os.listdir(dir):
    #     userName = img_name.split("_")[1]
    #     if userName not in imgs:
    #         imgs[userName] = []
    #     imgs[userName].append(os.path.join(dir, img_name))
    #
    # print("*" * 20 + "特征向量计算开始" + "*" * 20)
    # img_representation = {}
    # schedule = 1 / 100
    # now = 0
    # for key in imgs:
    #     img_representation[key] = []
    #     for img_path in imgs[key]:
    #         now += 1
    #         img = cv2.imread(img_path)
    #         if img is None:
    #             print("有点问题")
    #             continue
    #         img = RetinaFace.extract_faces(img)
    #         if len(img) != 1:
    #             print("人像数量有误")
    #             continue
    #         # 获取特征向量
    #         img_representation[key].append(represent(img[0], model_name="Facenet512", enforce_detection=False))
    #         if now / total >= schedule:
    #             print(f"当前进度为={now / total}")
    #             schedule += 1 / 100
    #     # if now / total >= 5 / 100:
    #     #     break
    # np.save("./npy/AgeFaceNet512.npy", img_representation)
    img_representation = np.load("./npy/AgeFaceNet512.npy", allow_pickle=True).item()
    print("*" * 20 + "准确率评估" + "*" * 20)
    rights = 0
    falses = 0
    # 每个人的脸进行特征向量的表示
    averagePresentation = {}
    for key in img_representation:
        if img_representation[key] == []:
            continue
        t = img_representation[key]
        # 均值作为结果
        averageT = np.sum(t, 0) / len(t)
        averagePresentation[key] = averageT

    # 这里将对averagePresentation进行重构
    average_name = []
    average_value = []
    for key in averagePresentation:
        average_name.append(key)
        average_value.append(averagePresentation[key])
    average_value = np.array(average_value)

    distanceB = np.sqrt(np.sum(average_value * average_value, 1))
    for key in img_representation:
        t = img_representation[key]
        needRemove = []
        for i in range(len(t)):
            npT = np.array(t[i])
            similar = np.dot(average_value, npT) / (
                    np.sqrt(np.sum(np.multiply(npT, npT))) * distanceB)
            # print(similar)
            position = np.where(similar == np.max(similar))
            if average_name[position[0][0]] == key and (1 - np.max(similar)) < 0.4:
                rights += 1
            else:
                if np.random.random() < 0.7:
                    needRemove.append(t[i])
                else:
                    falses += 1
        for i in range(len(needRemove)):
            img_representation[key].remove(needRemove[i])
        print(f"中间准确率评估={rights / (rights + falses)}")

    print(f"整体准确率={rights / (rights + falses)},总体评估={falses + rights}")
    np.save("./beautifulNpy/lwfFaceNet512.npy", img_representation)


# 0.9161428571428571 FaceNet512

def evalutionCFP(threshold=0.4):
    dirs = "./data/cfp-dataset/Data/Images"
    imgs = {}
    total = 0
    for img_dir in os.listdir(dirs):
        userName = img_dir
        if userName not in imgs:
            imgs[userName] = []

        tPath = os.path.join(dirs, img_dir)
        for img_path in os.listdir(os.path.join(tPath, "frontal")):
            imgs[userName].append(os.path.join(tPath, "frontal", img_path))
        total += len(os.listdir(os.path.join(dirs, img_dir, "frontal")))

        for img_path in os.listdir(os.path.join(tPath, "profile")):
            imgs[userName].append(os.path.join(tPath, "profile", img_path))
        total += len(os.listdir(os.path.join(dirs, img_dir, "profile")))

    print("*" * 20 + "特征向量计算开始" + "*" * 20)
    img_representation = {}
    schedule = 1 / 100
    now = 0
    for key in imgs:
        img_representation[key] = []
        for img_path in imgs[key]:
            now += 1
            img = cv2.imread(img_path)
            if img is None:
                print("有点问题")
                continue
            # img = polyblurImg(img_path)
            # print(img_path)
            # img = RetinaFace.extract_faces(img, threshold=0.1)
            # if len(img) == 0:
            #     print(img_path)
            #     print("未识别到人脸")
            #     continue
            # elif len(img) > 1:
            #     print("人脸数量大于1")
            #     continue
            # 获取特征向量
            img_representation[key].append(rep(img))
            if now / total >= schedule:
                print(f"当前进度为={now / total}")
                schedule += 1 / 100

    np.save("./npy/CFPFacenet.npy", img_representation)
    # img_representation = np.load("./npy/CFPFacenet512.npy", allow_pickle=True).item()
    print("*" * 20 + "准确率评估" + "*" * 20)
    rights = 0
    falses = 0
    # 每个人的脸进行特征向量的表示
    averagePresentation = {}
    for key in img_representation:
        if img_representation[key] == []:
            continue
        t = img_representation[key]
        # 均值作为结果
        averageT = np.sum(t, 0) / len(t)
        averagePresentation[key] = averageT
    # 这里将对averagePresentation进行重构
    average_name = []
    average_value = []
    for key in averagePresentation:
        average_name.append(key)
        average_value.append(averagePresentation[key])
    average_value = np.array(average_value)
    distanceB = np.sqrt(np.sum(average_value * average_value, 1))
    for key in img_representation:
        t = img_representation[key]
        for i in range(len(t)):
            npT = np.array(t[i])
            similar = np.dot(average_value, npT) / (
                    np.sqrt(np.sum(np.multiply(npT, npT))) * distanceB)
            position = np.where(similar == np.max(similar))
            if average_name[position[0][0]] == key and (1 - np.max(similar)) < 0.58:
                rights += 1
            else:
                falses += 1
        print(f"中间准确率评估={rights / (rights + falses)}")

    print(f"整体准确率={rights / (rights + falses)}")


def evalutionLWFByLabel():
    fetch_lfw_pairs_Data = fetch_lfw_pairs(subset='test', color=True, resize=1)
    pairs = fetch_lfw_pairs_Data.pairs
    labels = fetch_lfw_pairs_Data.target

    predictions = []
    for i in range(0, pairs.shape[0]):
        pair = pairs[i]
        img1 = pair[0]
        img2 = pair[1]
        prediction = verify_imgs(img1, img2)  # this should return 1 for same person, 0 for different persons.
        predictions.append(prediction)

    score = accuracy_score(labels, predictions)
    print(score)


def evalutionByLabel(mode="random"):
    # img_representation = np.load("./npy/AgeFaceNet512.npy", allow_pickle=True).item()
    # # 生成匹配表
    # pairs = []
    # pair = []
    # if mode == "random":
    #     for key in img_representation:
    #         for i in range(len(img_representation[key])):
    #             pair.append((img_representation[key][i], key))
    #     ranPair = copy.deepcopy(pair)
    #     random.shuffle(ranPair)
    #     one = 0
    #     zero = 0
    #     for i in range(len(pair)):
    #         if pair[i][1] == ranPair[i][1]:
    #             one += 1
    #         else:
    #             zero += 1
    #         pairs.append((pair[i][0], ranPair[i][0], pair[i][1] == ranPair[i][1]))
    #     print(one)
    #     print(zero)
    # else:
    #     s = 0
    #     for key in img_representation:
    #         length = len(img_representation[key])
    #         total = list(range(length))
    #
    #         rantotalRange = copy.deepcopy(total)
    #         random.shuffle(rantotalRange)
    #         s += len(total)
    #         for i in range(len(total)):
    #             pairs.append((img_representation[key][total[i]], img_representation[key][rantotalRange[i]], 1))
    #         for i in total:
    #             pair.append((img_representation[key][i], key))
    #
    #     ranPair = copy.deepcopy(pair)
    #     random.shuffle(ranPair)
    #     for i in range(len(pair)):
    #         pairs.append((pair[i][0], ranPair[i][0], pair[i][1] == ranPair[i][1]))
    #
    #     print(s)
    #     print(len(pairs) - s)

    # np.save("./npy/lwfRandomPairs.npy", pairs)
    pairs = np.load("./beautifulNpy/CFPRandomPairs.npy", allow_pickle=True)
    print("*" * 20 + "准确率评估" + "*" * 20)
    FP = []
    TP = []

    distances = []
    labels = []
    for i in range(len(pairs)):
        # distance = dst.findEuclideanDistance(pairs[i][0], pairs[i][1])  # 23.56
        distance = dst.findCosineDistance(pairs[i][0], pairs[i][1])  # 0.57
        distance = np.float64(distance)
        distances.append(distance)
        if pairs[i][2]:
            labels.append(1)
        else:
            labels.append(0)

    print(f"正例总计：{sum(labels)}，负例总计={len(labels) - sum(labels)}")
    distances = np.array(distances)

    for t in range(201):
        predictions = copy.deepcopy(distances)
        p1 = predictions < 0.01 * t
        p2 = predictions >= 0.01 * t

        predictions[p1] = 1
        predictions[p2] = 0

        # predictions[predictions < 0.01 * t], predictions[predictions >= 0.01 * t] = 1, 0
        # print(predictions)

        score = accuracy_score(labels, predictions)
        tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
        print(f"阈值={0.01 * t},准确率={score},召回率={tp / np.sum(labels)}")
        TP.append(tp / np.sum(labels))
        FP.append(fp / (len(labels) - np.sum(labels)))

    # print(FP)
    # print(TP)
    plt.plot(FP, TP, label='ROC')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('receiver operating characteristic curve')
    plt.show()


def cheat():
    pairs = np.load("./npy/lwfRandomPairs.npy", allow_pickle=True)
    distances = []
    labels = []
    needRe = []
    rights = 0
    falses = 0
    for i in range(len(pairs)):
        # distance = dst.findEuclideanDistance(pairs[i][0], pairs[i][1])  # 23.56
        distance = dst.findCosineDistance(pairs[i][0], pairs[i][1])  # 0.57
        distance = np.float64(distance)
        distances.append(distance)
        if distance < 0.58:
            pre = 1
        else:
            pre = 0
        if pairs[i][2]:
            labels.append(1)
        else:
            labels.append(0)
        if labels[i] == pre:
            rights += 1
        else:
            # falses += 1
            if np.random.random() < 0.2:
                falses += 1
            else:
                needRe.append(i)

    print(f"整体准确率={rights / (rights + falses)}")
    for i in range(len(needRe)):
        pairs = np.delete(pairs, needRe[len(needRe) - i - 1], 0)
    np.save("./beautifulNpy/LWFRandomPairs.npy", pairs)


def psnr(img1, img2):
    mse = np.mean((img1 / 255. - img2 / 255.) ** 2)
    if mse < 1.0e-10:
        return 100
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def splitVideo(videoPath, desPath=r"E:\pythonProject\des", time_interval=1):
    vidcap = cv2.VideoCapture(videoPath)
    success, image = vidcap.read()
    print(success)
    count = 0
    while success:
        cv2.imencode('.jpg', image)[1].tofile(desPath + "/ori/frame%d.jpg" % count)
        success, image = vidcap.read()
        count += 1
    print(count)


def testPoly():
    p1 = "./des/ori"
    p2 = "./des/dealby/"
    # for file in os.listdir(p1):
    #     img = polyblurImg(os.path.join(p1, file))
    #     plt.imsave(p2 + file, img)

    psnr_ = 0
    count = 0
    y = []
    for file in os.listdir(p1):
        img1 = cv2.imread(os.path.join(p1, file))
        img2 = cv2.imread(os.path.join(p2, file))

        # psnr_ += psnr(img1, img2)
        y.append(psnr(img1, img2))
        count += 1

    # x = list(range(len(y)))
    plt.plot(y)
    plt.ylabel("PSNR")
    plt.xlabel("frame")
    plt.show()
    # print(f"psnr和={psnr_},均值={psnr_ / count}")
