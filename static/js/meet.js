var pc = null;
var localVideo = document.querySelector("video#localVideo");
var localAudio = document.querySelector('#localAudio');
var localDisplay = document.querySelector('#localDisplay');


function negotiate () {
	return pc.createOffer().then(function (offer) {
		return pc.setLocalDescription(offer);
	}).then(function () {
		// wait for ICE gathering to complete
		return new Promise(function (resolve) {
			if (pc.iceGatheringState === 'complete') {
				resolve();
			} else {
				function checkState () {
					if (pc.iceGatheringState === 'complete') {
						pc.removeEventListener('icegatheringstatechange', checkState);
						resolve();
					}
				}
				pc.addEventListener('icegatheringstatechange', checkState);
			}
		});
	}).then(function () {
		var offer = pc.localDescription;
		return fetch('/offer', {
			body: JSON.stringify({
				sdp: offer.sdp,
				type: offer.type,
				username: "ljz"
			}),
			headers: {
				'Content-Type': 'application/json'
			},
			method: 'POST'
		});
	}).then(function (response) {
		return response.json();
	}).then(function (answer) {
		return pc.setRemoteDescription(answer);
	}).catch(function (e) {
		alert(e);
	});
}


async function start () {
//    await navigator.mediaDevices.getUserMedia({
//        video: {
//            height: 360,
//            width: 480,
//        }
//
//    }).then(stream => {
//        localVideo.srcObject = stream;
//        localVideo.addEventListener('loadedmetadata', () => {
//            localVideo.play();
//        });
//    });

    await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true,
    }).then(stream => {
        localVideo.srcObject = stream;
        localVideo.addEventListener('loadedmetadata', () => {
            localVideo.play();
            localAudio.play();
        });
    });


//	var config = {
//		sdpSemantics: 'unified-plan',
//		iceServers: [{ urls: ['stun:stun.l..com:19302'],
//		}]
//	};
//
//	pc = new RTCPeerConnection(config);
//
//	localVideo.srcObject.getVideoTracks().forEach(track => {
//		pc.addTrack(track);
//	});
//
//	localAudio.srcObject.getAudioTracks().forEach(track => {
//		pc.addTrack(track);
//	});
//
//	document.getElementById('start').style.display = 'none';
//	negotiate();
//	document.getElementById('stop').style.display = 'inline-block';
}



function share () {
    navigator.mediaDevices.getDisplayMedia({
        video: true
    }).then(stream => {
        localDisplay.srcObject = stream;
        localDisplay.addEventListener('loadedmetadata', () => {
            localDisplay.play();
        });
    });
	var config = {
		sdpSemantics: 'unified-plan',
		iceServers: [{ urls: ['stun:stun.l..com:19302'],
		}]
	};

	pc = new RTCPeerConnection(config);

	localDisplay.srcObject.getVideoTracks().forEach(track => {
		pc.addTrack(track);
	});

//	document.getElementById('start').style.display = 'none';
	negotiate();
//	document.getElementById('stop').style.display = 'inline-block';
}


function stop () {
	document.getElementById('stop').style.display = 'none';
	setTimeout(function () {
		pc.close();
	}, 500);
}