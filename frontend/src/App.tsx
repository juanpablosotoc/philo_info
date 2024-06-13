import React from 'react';
import './App.css';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Home, { loader as homeLoader} from "./pages/home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoginSignup, { loginAction, loader as loginSignupLoader, signupAction } from './pages/LoginSignup';

const router = createBrowserRouter([
  {
    path: "/",
    errorElement: <h1>Hello</h1>,
    children: [
      { index: true, element: <Home />, loader: homeLoader},
      { path: 'login', element: <LoginSignup type="login" />, action: loginAction, loader: loginSignupLoader},
      { path: 'signup', element: <LoginSignup type="signup" />, loader: loginSignupLoader, action: signupAction},
    ],
  },
]);

function App() {
  return <GoogleOAuthProvider clientId="881148832718-aukuvpi4g0rhc04sfg8q09btdo392fs3.apps.googleusercontent.com"><RouterProvider router={router}></RouterProvider></GoogleOAuthProvider>
}

export default App;

// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <Root></Root>,
//     errorElement: <ErrorPage></ErrorPage>,
//     children: [
//       { index: true,element: <Home></Home>},
//       { path: "about_us", element: <About></About> },
//       { path: 'products', element: <Products />},
//       { path: 'products/:id', element: <Product></Product>}
//     ],
//   },
// ]);