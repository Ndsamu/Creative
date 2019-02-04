// Caching the DOM (document object model - tree structure)
let userScore = 0;
let computerScore = 0;
const userScore_span = document.getElementById("user-score");
const computerScore_span = document.getElementById("comp-score");
const scoreBoard_div = document.querySelector(".score-board");
const crown_img = document.getElementById("crown")
const result_p = document.querySelector(".result > p");
const rock_div = document.getElementById("r");
const paper_div = document.getElementById("p");
const scissor_div = document.getElementById("s");

function convertToWord(choice) {
  switch (choice) {
    case 'r':
      return "Rock";
    case 'p':
      return "Paper";
    case 's':
      return "Scissor";
  }
}

function getComputerChoice() {
  const choices = ['r','p','s'];
  return choices[Math.floor(Math.random() * 3)];
}

function win(userChoice, computerChoice) {
  userScore++;
  userScore_span.innerHTML = userScore;
  result_p.innerHTML = `${convertToWord(userChoice)} beats ${convertToWord(computerChoice)}. You win!`;
  document.getElementById('crown').style.left="-100px";
  document.getElementById('crown').style.display="block";
  document.getElementById(userChoice).parentElement.classList.add('green-glow');
  setTimeout(function() { document.getElementById(userChoice).parentElement.classList.remove('green-glow') }, 1000);
}

function loss(userChoice, computerChoice) {
  computerScore++;
  computerScore_span.innerHTML = computerScore;
  result_p.innerHTML = `${convertToWord(userChoice)} loses to ${convertToWord(computerChoice)}. You lose.`;
  document.getElementById('crown').style.left="250px";
  document.getElementById('crown').style.display="block";
  document.getElementById(userChoice).parentElement.classList.add('red-glow');
  setTimeout(function() { document.getElementById(userChoice).parentElement.classList.remove('red-glow') }, 1000);
}

function draw(userChoice, computerChoice) {
  result_p.innerHTML = `${convertToWord(userChoice)} ties with ${convertToWord(computerChoice)}. Draw.`;
  document.getElementById('crown').style.display="none";
  document.getElementById(userChoice).parentElement.classList.add('grey-glow');
  setTimeout(function() { document.getElementById(userChoice).parentElement.classList.remove('grey-glow') }, 1000);
}

function game(userChoice) {
  computerChoice = getComputerChoice();
  switch (userChoice + computerChoice) {
    case "rs":
    case "pr":
    case "sp":
      win(userChoice, computerChoice);
      break;
    case "sr":
    case "rp":
    case "ps":
      loss(userChoice, computerChoice);
      break;
    case "rr":
    case "pp":
    case "ss":
      draw(userChoice, computerChoice);
      break;
  }
}

function main() {
  rock_div.addEventListener('click',function() {
    game("r");
  })

  paper_div.addEventListener('click',function() {
    game("p");
  })

  scissor_div.addEventListener('click',function() {
    game("s");
  })
}

main();
