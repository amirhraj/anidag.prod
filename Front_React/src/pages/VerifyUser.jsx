import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import $api from "../api/auth"; // твой axios-инстанс
import styles from "./VerifyUser.module.css";

export default function VerifyUser() {
  const { token } = useParams();
  // console.log(token)
  const navigate = useNavigate();

  const [status, setStatus] = useState("pending");
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    if (!token) {
      setStatus("invalid");
      return;
    }

    setLoading(true);
    try {
      const response = await $api.get(`/verify/${token}`);
      if (response.status === 200) {
        setStatus("success");
        setTimeout(() => navigate("/"), 2000);
      }
    } catch (error) {
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  // Автоматически запускаем проверку при загрузке
  useEffect(() => {
    handleVerify();
  }, [token]);

  return (
    <div>

      <div className={styles.middle_content}>
        {status === "pending" && (
          <p>Подтверждение аккаунта...</p>
        )}
        {status === "success" && <p>Аккаунт подтвержден! Перенаправление...</p>}
        {status === "error" && <p>Ошибка подтверждения. Попробуйте снова.</p>}
        {status === "invalid" && <p>Неверная ссылка подтверждения.</p>}
      </div>

    </div>
  );
}
