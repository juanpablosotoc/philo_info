import React from 'react';
import './App.css';
import Assets from './pages/Assets';

// import Root from "./pages/Root";
import Home from "./pages/home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// import About from "./pages/About";
import Error from "./pages/Error";
// import Product from "./pages/Product";
// import Products from "./pages/Products";
import LoginSignup from './pages/LoginSignup';

const router = createBrowserRouter([
  {
    path: "/",
    errorElement: <Error></Error>,
    children: [
      { index: true,element: <Home></Home>},
      { path: 'login', element: <LoginSignup type="login" />},
      { path: 'signup', element: <LoginSignup type="signup" />}
    ],
  },
]);

function App() {
  return <RouterProvider router={router}></RouterProvider>;
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