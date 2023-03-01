var pc = null;
var localVideo = document.querySelector("video#localVideo");
var serverVideo = document.querySelector("video#serverVideo");
var localAudio = document.querySelector('#localAudio');
var serverAudio = document.querySelector('#serverAudio');



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
				username: "yyy",
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

function receive () {
    navigator.mediaDevices.getUserMedia({
        video: {
            height: 360,
            width: 480,
        }
    }).then(stream => {
        localVideo.srcObject = stream;
        localVideo.addEventListener('loadedmetadata', () => {
            localVideo.play();
        });
    });

    navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
    }).then(stream => {
        localAudio.srcObject = stream;
        localAudio.addEventListener('loadedmetadata', () => {
        });
    });


	var config = {
		sdpSemantics: 'unified-plan',
		iceServers: [{ urls: ['stun:stun.l..com:19302'],
		}]
	};

	pc = new RTCPeerConnection(config);

	localVideo.srcObject.getVideoTracks().forEach(track => {
		pc.addTrack(track);
	});
	pc.addEventListener('track', function (evt) {
		console.log("receive server video");
		if (evt.track.kind == 'video') {
			serverVideo.srcObject = evt.streams[0];
		}
	});

	pc.addEventListener('track', function (evt) {
		console.log("receive server audio");
		if (evt.track.kind == 'audio') {
			serverAudio.srcObject = evt.streams[0];
		}
	});

	document.getElementById('receive').style.display = 'none';
	negotiate();
	document.getElementById('stop').style.display = 'inline-block';
}

function stop () {
	document.getElementById('stop').style.display = 'none';
	setTimeout(function () {
		pc.close();
	}, 500);
}