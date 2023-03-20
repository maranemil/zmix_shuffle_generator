/*
##########################################################################
jquery
##########################################################################

https://jsfiddle.net/
https://www.onlinehtmleditor.net/
https://liveweave.com/
https://vscode.dev/
https://css-tricks.com/snippets/javascript/select-random-item-array/
*/

$(function() {
    // https://github.com/pffy/wav-piano-sound/tree/main/wav
    const arr_piano = [
        'a1.wav',
        "a1s.wav",
        "b1.wav",
        "c1.wav",
        "c1s.wav",
        "c2.wav",
        "d1.wav",
        "d1s.wav",
        "e1.wav",
        "f1.wav",
        "f1s.wav",
        "g1.wav",
        "g1s.wav"
    ];

    //const urlpiano = "https://github.com/pffy/wav-piano-sound/blob/main/wav/";
    //const raw = "?raw=true";
    const urlpiano = "./wav/"
    const raw = "";

    $('.sound').click(function() {
        let note = arr_piano[Math.floor(Math.random() * arr_piano.length)];
        console.log(note)
        var audio = new Audio(urlpiano + note + raw);
        audio.play();
    });
});

