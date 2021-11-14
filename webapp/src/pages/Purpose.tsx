import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

import CTACard from "../components/CTACard";
import Gallery from "../components/Gallery";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    media: {
      height: "240px",
    },
    splash: {
      display: "block",
      margin: "40px auto",
      width: "80%",
      backgroundColor: "#cccccc",
    },
    backgroundImage: {
      position: "fixed",
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
      opacity: 0.25,
      zIndex: -100,
      height: "100%",
      background:
        "url(https://www.pngkit.com/png/detail/194-1940853_play-connect-4-with-iphone-ipad-using-imessage.png) no-repeat center center fixed",
      backgroundSize: "cover",
    },
    overlay: {
      position: "fixed",
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
      opacity: 0.35,
      zIndex: -100,
      height: "100%",
      backgroundColor: "#000000",
      backgroundSize: "cover",
    },
    main: {
      textAlign: "center",
      paddingTop: "5vh"
    },
    purposeMain: {
      fontSize: "2em",
    },
    purposeSub: {
      fontSize: "1.5em",
    },
  })
);

export default function Purpose() {
  const classes = useStyles();

  return (
    <main className={classes.main}>
      <div className={classes.backgroundImage}/>
      <div className={classes.overlay}/>
      <h1>Our Purpose</h1>
      <section className={classes.purposeMain}>
        This website provides some tutorials of general algorithms and uses of
        them we have learned from CSC 480 and/or our group project.
      </section>
      <section className={classes.purposeSub}>
        Please visit our GitHub repo linked below in the footer to view all source code used in this project. More advanced usage of some of the algorithms described in our tutorials can be found in the files in <a href="https://github.com/CSC480-Group1/CSC-480/tree/main/code/games">this directory</a>.
      </section>
    </main>
  );
}
