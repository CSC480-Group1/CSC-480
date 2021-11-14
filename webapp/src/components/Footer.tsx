import { AppBar, Typography } from "@material-ui/core";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import { Link } from "react-router-dom";
import { tutorials } from "../data";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      overflow: "hidden",
      padding: "40px 0"
    },
    grid: {
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "space-between",
      width: "80%",
      margin: "0 auto",
      "& h3 a": {
        color: "white"
      },
      "& a": {
        display: "block",
        margin: "16px 0",
        color: "#ddd"
      },
      "& div": {
        display: "inline-block"
      }
    },
    siteTag: {
      width: "40%",
      minWidth: "300px",
      marginBottom: "30px"
    },
    linkTag: {
      width: "16.6%",
      minWidth: "200px",
      paddingRight: "3px"
    }
  })
);

export default function Footer() {
  const classes = useStyles();
  
  return (
    <AppBar position="static" component="footer" className={classes.root}>
      <div className={classes.grid}>
        <div className={classes.siteTag}>
          <h2>Search Algorithms in Games</h2>
          <p>CSC 480 | Dr. Canaan | Fall 2021 | Cal Poly</p>
          <Typography variant="subtitle2">
            Ben Glossner  |  Jordan Powers <br/> Mukhammadorif Sultanov  |  Nicholas Sheffler
          </Typography>
        </div>
        <div className={classes.linkTag}>
          <h3>Introduction</h3>
          <Link to='/purpose'>Purpose</Link>
        </div>
        
        <div className={classes.linkTag}>
          <h3>Tutorials</h3>
          {tutorials.map((tutorial, idx) =>
            <Link key={`footer-link-${idx}`} to={`/${tutorial.notebook}`}>{tutorial.content.title}</Link>
          )}
        </div>
        
        <div className={classes.linkTag}>
          <h3>Resources</h3>
          <a
            href="https://github.com/CSC480-Group1/CSC-480"
            target="_blank"
            rel="noreferrer noopener"
          >
            GitHub
          </a>
          <a
            href="https://github.com/CSC480-Group1/CSC-480/tree/main/code/notebooks"
            target="_blank"
            rel="noreferrer noopener"
          >
            Notebooks
          </a>
        </div>
      </div>
    </AppBar>
  );
}
