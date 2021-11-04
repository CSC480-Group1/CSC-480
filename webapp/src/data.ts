export const tutorials = [
  /*Scikit Learn Classifier*/
  {
    img: {
      url: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png",
      title: "Scitkit Learn Logo"
    },
    content: {
      title: "Scikit Learn Classifier",
      description:
        "Using the decision tree classifier we implemented in the previous" +
        " tutorial, we will now transform that into a classifier that works" +
        " with sklearn",
      dataset: "heart.csv",
      questions: [
        {
          question: "Why do you think `check_estimator` has no output if it succeeded? What might it do if it failed?",
          answer: "`check_estimator` is basically doing unit testing on your estimator. When it fails, an error is raised. Thus no errors raised means all the checks succeeded."
        }
      ]
    },
    notebook: "heart_classifier_with_sklearn"
  },
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
