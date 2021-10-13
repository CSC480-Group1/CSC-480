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
  }
];
