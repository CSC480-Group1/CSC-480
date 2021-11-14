import { AppBar, Link, Toolbar } from "@material-ui/core";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import React from "react";
import {Link as RouterLink} from "react-router-dom";
import { ConnectX } from "../connectx/ConnectX";

// TODO: collapse links into hamburger menu on small screen
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    heading: {
      color: "white"
    },
    bar: {
      justifyContent: "space-between"
    },
    links: {
      color: "white",
      padding: "0 12px"
    }
  })
);

export default function ButtonAppBar() {
  const classes = useStyles();
  
  return (
    <AppBar position="static">
      <Toolbar className={classes.bar}>
        <Link to="/" component={RouterLink}>
          <h3 className={classes.heading}>
            Search Algorithms in Games
          </h3>
        </Link>
        <span>
          <Link className={classes.links} to="/" component={RouterLink}>
            Home
          </Link>
          <Link className={classes.links} to="/connectx-demo" component={RouterLink}>
            Connect X
          </Link>
        </span>
      </Toolbar>
    </AppBar>
  );
}
