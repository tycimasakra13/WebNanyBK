console.log("test watch js");
document.addEventListener("DOMContentLoaded", function() {
    // Code to be executed when the DOM is ready
  //  const ws = new WebSocket("ws://127.0.0.1:5000/stream")
    //const socket = io.connect();
    const videoElement = document.getElementById("videoElement");
    const frameRate = 1;
    const framePath = "stream_feed"
    const totalFrames = 100;

    let frameIndex = 1;
    const img = document.getElementById("imgElement");
    //
    // ws.addEventListener("connect", () => {
    //     console.log("websocket conn");
    // });



    function loadAndPlayVideo() {
        if (frameIndex <= totalFrames) {
            const filename = `frame_${frameIndex}.jpg`;
            const frameSrc = `${framePath}/${frameIndex}`;

            //videoElement.src = frameSrc;
            //videoElement.src = frameSrc;
            img.src = frameSrc;
            frameIndex++;
        } else {
            frameIndex = 1;
        }

        setTimeout(loadAndPlayVideo);
    }

   // loadAndPlayVideo();
});