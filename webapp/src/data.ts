export const tutorials = [
  /* Minimax basic */
  {
    img: {
      url: "https://i.ytimg.com/vi/KU9Ch59-4vw/maxresdefault.jpg",
      title: "Minimax Algorithm Image"
    },
    content: {
      title: "Minimax with Connect X",
      description:
        "We will implement the minimax algorithm from scratch and test it on Connect X (modification of Connect 4).",
      dataset: "",
      questions: [
        {
          question: "Why do you think we only used a 3x3 or 3x4 board?",
          answer: "A couple reasons. For one, it's easier to conceptualize. The bigger reason though is because minimax is not efficient on its own. It will check every possible combination each move, which is a lot, even for a 3x4 board at first."
        }
      ]
    },
    notebook: "minimax_algorithm"
  },
  // MCTS
  {
    img: {
      url: "https://miro.medium.com/max/1000/1*OpJz2LcElVB_XPEYAvK87Q.jpeg",
      title: "MCTS Algorithm Image"
    },
    content: {
      title: "Monte Carlo Tree Search with Connect X",
      description:
        "We will implement the Monte Carlo Tree Search (MCTS) algorithm from scratch and test it on Connect X (modification of Connect 4).",
      dataset: "",
      questions: [
        {
          question: "What's the tradeoff of using a high number of iterations? Why not make it a very large number?",
          answer: "The higher the number of iterations, the paths that MCTS will create, which takes more time. We need to have a happy medium of time it takes to complete the guess for the best move and how good that guess is."
        }
      ]
    },
    notebook: "mcts_tutorial"
  },
];
