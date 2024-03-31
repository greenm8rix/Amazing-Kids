var tones = [
  new Audio("static/src/assets/gameaudio/audios\\1.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\2.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\3.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\4.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\5.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\6.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\7.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\8.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\9.mp3"),
  new Audio("static/src/assets/gameaudio/audios\\10.mp3"),
];

var buttons = [
  "but1",
  "but2",
  "but3",
  "but4",
  "but5",
  "but6",
  "but7",
  "but8",
  "but9",
  "but10",
];

var wrongAnswer = new Audio(
  "static/src/assets/gameaudio/audios\\wrong_sound.mp3"
);
var rightAnswer = new Audio(
  "static/src/assets/gameaudio/audios\\right_sound.mp3"
);
var level = 1;

var level1Answer = [4, 3, 2];
var level2Answer = [0, 1, 9, 4, 3, 2];
var level3Answer = [8, 7, 6, 5, 4, 3];
var userAnswer = [];
var index = 0;

document.getElementById("replay").onclick = function () {
  whiteAllButtons();
  clearPlayList();
  document.getElementById("wrong").style.display = "none";
  index = 0;
  for (x = 0; x < userAnswer.length; ) {
    userAnswer.pop();
  }

  pauseAllButtons();
  if (level == 1) {
    level1();
  } else if (level == 2) {
    level2();
  } else if (level == 3) {
    level3();
  }
};

document.getElementById("submit").onclick = function () {
  document.getElementById("wrong").style.display = "none";
  whiteAllButtons();
  clearPlayList();
  for (i = 0; i < userAnswer.length; i++) {
    if (level == 1) {
      if (userAnswer[i] != level1Answer[i]) {
        wrongAnswer.play();
        for (x = 0; x < userAnswer.length; ) {
          userAnswer.pop();
        }
        index = 0;
        document.getElementById("wrong").style.display = "block";
        return;
      }
    }
    if (level == 2) {
      if (userAnswer[i] != level2Answer[i]) {
        wrongAnswer.play();
        for (x = 0; x < userAnswer.length; ) {
          userAnswer.pop();
        }
        index = 0;
        document.getElementById("wrong").style.display = "block";
        return;
      }
    }
    if (level == 3) {
      if (userAnswer[i] != level3Answer[i]) {
        wrongAnswer.play();
        for (x = 0; x < userAnswer.length; ) {
          userAnswer.pop();
        }
        index = 0;
        document.getElementById("wrong").style.display = "block";
        return;
      }
    }
  }
  rightAnswer.play();

  for (x = 0; x < userAnswer.length; ) {
    userAnswer.pop();
  }
  index = 0;

  if (level != 4) {
    level++;
    document.getElementById("level").innerHTML = "level " + level;
  }
};

document.getElementById("but1").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but1").style.backgroundColor = "orange";
  tones[0].play();
  userAnswer[index] = 0;
  index++;
};

document.getElementById("but2").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but2").style.backgroundColor = "orange";
  tones[1].play();
  userAnswer[index] = 1;
  index++;
};

document.getElementById("but3").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but3").style.backgroundColor = "orange";
  tones[2].play();
  userAnswer[index] = 2;
  index++;
};

document.getElementById("but4").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but4").style.backgroundColor = "orange";
  tones[3].play();
  userAnswer[index] = 3;
  index++;
};

document.getElementById("but5").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but5").style.backgroundColor = "orange";
  tones[4].play();
  userAnswer[index] = 4;
  index++;
};

document.getElementById("but6").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but6").style.backgroundColor = "orange";
  tones[5].play();
  userAnswer[index] = 5;
  index++;
};

document.getElementById("but7").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but7").style.backgroundColor = "orange";
  tones[6].play();
  userAnswer[index] = 6;
  index++;
};

document.getElementById("but8").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but8").style.backgroundColor = "orange";
  tones[7].play();
  userAnswer[index] = 7;
  index++;
};

document.getElementById("but9").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but9").style.backgroundColor = "orange";
  tones[8].play();
  userAnswer[index] = 8;
  index++;
};

document.getElementById("but10").onclick = function () {
  clearPlayList();
  pauseAllButtons();
  whiteAllButtons();
  document.getElementById("but10").style.backgroundColor = "orange";
  tones[9].play();
  userAnswer[index] = 9;
  index++;
};

function whiteAllButtons() {
  for (i = 0; i < 10; i++) {
    document.getElementById(buttons[i]).style.background = "white";
  }
}
function pauseAllButtons() {
  for (i = 0; i < 10; i++) {
    tones[i].pause();
  }
}
function level1() {
  tones[4].play();
  document.getElementById(buttons[4]).style.background = "orange";

  tones[4].onended = function () {
    document.getElementById(buttons[4]).style.background = "white";
    tones[3].play();
    document.getElementById(buttons[3]).style.background = "orange";

    tones[3].onended = function () {
      document.getElementById(buttons[3]).style.background = "white";
      tones[2].play();
      document.getElementById(buttons[2]).style.background = "orange";

      tones[2].onended = function () {
        document.getElementById(buttons[2]).style.background = "white";
      };
    };
  };
}
function level3() {
  tones[8].play();
  document.getElementById(buttons[8]).style.background = "orange";

  tones[8].onended = function () {
    document.getElementById(buttons[8]).style.background = "white";
    tones[7].play();
    document.getElementById(buttons[7]).style.background = "orange";

    tones[7].onended = function () {
      document.getElementById(buttons[7]).style.background = "white";
      tones[6].play();
      document.getElementById(buttons[6]).style.background = "orange";

      tones[6].onended = function () {
        document.getElementById(buttons[6]).style.background = "white";
        tones[5].play();
        document.getElementById(buttons[5]).style.background = "orange";

        tones[5].onended = function () {
          document.getElementById(buttons[5]).style.background = "white";
          tones[4].play();
          document.getElementById(buttons[4]).style.background = "orange";

          tones[4].onended = function () {
            document.getElementById(buttons[4]).style.background = "white";
            tones[3].play();
            document.getElementById(buttons[3]).style.background = "orange";

            tones[3].onended = function () {
              document.getElementById(buttons[3]).style.background = "white";
            };
          };
        };
      };
    };
  };
}
function level2() {
  tones[0].play();
  document.getElementById(buttons[0]).style.background = "orange";

  tones[0].onended = function () {
    document.getElementById(buttons[0]).style.background = "white";
    tones[1].play();
    document.getElementById(buttons[1]).style.background = "orange";

    tones[1].onended = function () {
      document.getElementById(buttons[1]).style.background = "white";
      tones[9].play();
      document.getElementById(buttons[9]).style.background = "orange";

      tones[9].onended = function () {
        document.getElementById(buttons[9]).style.background = "white";
        tones[4].play();
        document.getElementById(buttons[4]).style.background = "orange";

        tones[4].onended = function () {
          document.getElementById(buttons[4]).style.background = "white";
          tones[3].play();
          document.getElementById(buttons[3]).style.background = "orange";

          tones[3].onended = function () {
            document.getElementById(buttons[3]).style.background = "white";
            tones[2].play();
            document.getElementById(buttons[2]).style.background = "orange";

            tones[2].onended = function () {
              document.getElementById(buttons[2]).style.background = "white";
            };
          };
        };
      };
    };
  };
}
function clearPlayList() {
  tones[0].onended = function () {};
  tones[1].onended = function () {};
  tones[2].onended = function () {};
  tones[3].onended = function () {};
  tones[4].onended = function () {};
  tones[5].onended = function () {};
  tones[6].onended = function () {};
  tones[7].onended = function () {};
  tones[8].onended = function () {};
  tones[9].onended = function () {};
}
