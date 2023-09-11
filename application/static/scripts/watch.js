console.log("test watch js");
document.addEventListener("DOMContentLoaded", function() {
    // Code to be executed when the DOM is ready

    var socket = io({
            cors: {
                origin: "http://localhost:5000/stream", // Specify your allowed origin
                //origin: "https://webnanyae.azurewebsites.net/stream",
                methods: ["GET", "POST"]
            }
        });

    let frameIndex = 1;
    const img = document.getElementById("imgElement");

     socket.on("connect", function () {
      console.log("Connected... watch!", socket.connected);
    });


    socket.on("disconnect", function () {
      console.log("disconnected watch!", socket.connected);
    });


     function loadAndPlayVideo() {
    //     if (frameIndex <= totalFrames) {
    //         const filename = `frame_${frameIndex}.jpg`;
    //         const frameSrc = `${framePath}/${frameIndex}`;
    //
    //         //videoElement.src = frameSrc;
    //         //videoElement.src = frameSrc;
    //         img.src = frameSrc;
    //         frameIndex++;
    //     } else {
    //         frameIndex = 1;
    //     }
    //
          socket.on('get_image', function () {
        console.log('get image');
    })
       setTimeout(loadAndPlayVideo);
     }

    loadAndPlayVideo();

         socket.on("processed_imageget", function (image) {
        console.log(image);
      img.setAttribute("src", image);
    });
});