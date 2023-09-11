console.log("test main js");


document.addEventListener("DOMContentLoaded", function() {
    // Code to be executed when the DOM is ready
    //var socket = io.connect();
    var socket = io({
            cors: {
                origin: "http://localhost:5000/stream", // Specify your allowed origin
                //origin: "https://webnanyae.azurewebsites.net/stream",
                methods: ["GET", "POST"]
            }
        });
    let camera_button = document.querySelector("#start-camera");
    let photo = document.querySelector("#imgElement");
    let video = document.querySelector("#video");
    let stop_button = document.querySelector("#stop-button");


    let camera_stream = null;
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
        socket.connect();
        sendFrameToServer();
    });

    console.log("isStreaming" + isStreaming);

    stop_button.addEventListener('click', function () {
        console.log('stop button');
        socket.disconnect();
        isStreaming = false;
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

            requestAnimationFrame(sendFrameToServer);
        }
    }

    socket.on("processed_image", function (image) {
      photo.setAttribute("src", image);
    });

});