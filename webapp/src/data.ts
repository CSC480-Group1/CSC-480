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
  }
];
