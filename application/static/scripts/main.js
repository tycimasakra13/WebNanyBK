console.log("test main js");


document.addEventListener("DOMContentLoaded", function() {
    // Code to be executed when the DOM is ready
    //var socket = io.connect();
    var socket = io({
            cors: {
                //origin: "http://localhost:5000/stream", // Specify your allowed origin
                origin: "https://webnanyae.azurewebsites.net/stream",
                methods: ["GET", "POST"]
            }
        });
    let camera_button = document.querySelector("#start-camera");
    let photo = document.querySelector("#imgElement");
    let video = document.querySelector("#video");
    let start_button = document.querySelector("#start-record");
    let stop_record = document.querySelector("#stop-record");
    let stop_button = document.querySelector("#stop-button");
    let download_link = document.querySelector("#download-video");

    let camera_stream = null;
    let media_recorder = null;
    let blobs_recorded = [];
    let isStreaming = false;


    socket.on("connect", function () {
      console.log("Connected...!", socket.connected);
    });

    socket.on("disconnect", function () {
      console.log("Connected...!", socket.connected);
    });

    camera_button.addEventListener('click', async function() {
        camera_stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        video.srcObject = camera_stream;
        isStreaming = true;
    });

    console.log("isStreaming" + isStreaming);
    start_button.addEventListener('click', function() {
        // set MIME type of recording as video/webm
        media_recorder = new MediaRecorder(camera_stream, { mimeType: 'video/webm' });

        // event : new recorded video blob available
        media_recorder.addEventListener('dataavailable', function(e) {
            blobs_recorded.push(e.data);
            e.data
        });

        // event : recording stopped & all blobs sent
        media_recorder.addEventListener('stop', function() {
            // create local object URL from the recorded video blobs
            let video_local = URL.createObjectURL(new Blob(blobs_recorded, { type: 'video/webm' }));
            download_link.href = video_local;
        });

        // start recording with each recorded blob having 1 second video
        media_recorder.start(1000);

        sendFrameToServer();
    });

    stop_record.addEventListener('click', function() {
        console.log('stop');
        media_recorder.stop();
        socket.disconnect();
        isStreaming = false;
    });

    stop_button.addEventListener('click', function () {
        console.log('stop button');
        camera_stream.stop();
    })

    function sendFrameToServer() {
        if (isStreaming) {
            const canvas = document.createElement("canvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const ctx = canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const frameData = canvas.toDataURL("image/jpeg");

            // fetch("/json_test", {
            //     method: "POST",
            //     body: JSON.stringify({frameData}),
            //     headers: {
            //         "Content-Type": "application/json",
            //     },
            // }).then((response)=>{
            //     if(!response.ok) {
            //         console.error("error sending frame to server.")
            //     }
            // });

            socket.emit('image', frameData);

            setTimeout(sendFrameToServer, 1000/30);
        }
    }

    socket.on("processed_image", function (image) {
      photo.setAttribute("src", image);
    });

});