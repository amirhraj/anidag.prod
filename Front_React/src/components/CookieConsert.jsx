import { useEffect, useState } from "react";
import "./cookieconsent.modules.css";

const CookieConsent = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [animationClass, setAnimationClass] = useState("cookie-hidden");

  useEffect(() => {
    const consent = localStorage.getItem("cookieConsent");
    if (!consent) {
      setIsVisible(true);
      setTimeout(() => setAnimationClass("cookie-visible"), 10);
    }
  }, []);

  const handleAccept = () => {
    setAnimationClass("cookie-hidden");
    setTimeout(() => {
      localStorage.setItem("cookieConsent", "true");
      setIsVisible(false);
    }, 500);
  };

  return (
    isVisible && (
      <div className={`cookie-consent ${animationClass}`}>
        <p className="cookie-text">Этот сайт использует куки для улучшения работы.</p>
        <button
          onClick={handleAccept}
          className="cookie-button"
        >
          Да, принимаю
        </button>
      </div>
    )
  );
};

export default CookieConsent;