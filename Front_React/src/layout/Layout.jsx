import Header from "../components/Header.jsx";
import Footer from "../components/Footer/Footer.jsx";
// import ThemeToggle from '../pages/ThemeToggle.jsx';

import React from "react";

const Layout = ({ children }) => {
  return (
    <>
  {/* <h1
  style={{
    color: '#9ca3af',
    backgroundColor: '#1a1a1a',
    fontSize: '30px',
    padding: '10px',
    borderRadius: '8px',
    textAlign: "center"
  }}
>
  Друзья, чтобы нам всем держаться вместе и не потерять друг друга, рекомендую телеграмм,
  если страницы не грузит, используйте программу для обхода блокировок 
</h1> */}
      <Header />
     
      <main>{children}</main>
      <Footer />
    </>
  );
};

export default Layout;
