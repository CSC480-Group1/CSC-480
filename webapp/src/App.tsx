import React from "react";
import { Switch, Route, HashRouter } from "react-router-dom";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import { Container } from "@material-ui/core/";
import Markdown from "./components/Markdown";
import { tutorials } from "./data";

import Home from "./pages/Home";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

const theme = createMuiTheme({
  palette: {
    primary: {
      light: "#62727b",
      main: "#37474f",
      dark: "#102027",
      contrastText: "#fff",
    },
    secondary: {
      light: "#60ad5e",
      main: "#2e7d32",
      dark: "#005005",
      contrastText: "#000",
    },
    background: {
      paper: "#f3f0e8"
    }
  },
});

function App() {
  return (
    <HashRouter>
      <ThemeProvider theme={theme}>
        <Navbar />
        <Container>
          <Switch>

            <Route exact path="/" component={Home} />
            {tutorials.map((tutorial) =>
              <Route path={`/${tutorial.notebook}`}>
                <Markdown
                  {...tutorial.content}
                  fileName={tutorial.notebook}
                />
              </Route>
            )}
          </Switch>
        </Container>
        <Footer />
      </ThemeProvider>
    </HashRouter>
  );
}

export default App;
