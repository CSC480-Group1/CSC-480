import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import React from "react";

import CTACard from "../components/CTACard";
import Gallery from "../components/Gallery";
import { tutorials } from "../data";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    card: {
      width: "30%",
      minWidth: "300px",
      margin: "10px 8px"
    },
    media: {
      height: "240px"
    },
    splash: {
      display: "block",
      margin: "40px auto",
      width: "80%",
      backgroundColor: "#cccccc"
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
      background: "url(https://www.pngkit.com/png/detail/194-1940853_play-connect-4-with-iphone-ipad-using-imessage.png) no-repeat center center fixed",
      backgroundSize: "cover"
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
      backgroundSize: "cover"
    }
  })
);

export default function Home() {
  const classes = useStyles();
  
  return (
    <>
      <div className={classes.backgroundImage}/>
      <div className={classes.overlay}/>
      <section>
        <h1>CSC 480 Project</h1>
        <p>Some game heuristics</p>
      </section>
      <CTACard
        title="Not sure where to start?"
        description="Learn how to use the website"
        buttonText="Get Started"
        linkTo="/getting-started"/>

      <Gallery cards={tutorials}/>
    </>
  );
}
