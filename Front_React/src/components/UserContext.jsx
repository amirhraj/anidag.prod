import { createContext, useContext, useEffect, useState } from 'react';
import $api from '../api/auth';

const UserContext = createContext(null);

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
  const [userData, setUserData] = useState(() => {
    const savedUser = localStorage.getItem("userData");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [loadingUser, setLoadingUser] = useState(true);

  useEffect(() => {
    if (userData) {
      localStorage.setItem("userData", JSON.stringify(userData));
    } else {
      localStorage.removeItem("userData");
    }
  }, [userData]);

  useEffect(() => {
    const fetchUser = async () => {
      const userId = localStorage.getItem("user_id");
      const token = localStorage.getItem("access_token");

      if (!userId || !token) {
        setLoadingUser(false);
        return;
      }

      try {
        const res = await $api.get(`/api/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const user = res.data;

        setUserData({
          id: user.id,
          username: user.name,
          avatar_url: user.avatar_url,
          likes: user.likes,
          dislikes: user.dislikes,
          views: user.views,
          background: {
            image_url: user.bk_image,
          },
          global_background: {
            image_url: user.bk_gl_image,
          },
        });
      } catch (error) {
        console.error("Ошибка при загрузке пользователя:", error);
      } finally {
        setLoadingUser(false);
      }
    };

    fetchUser();
  }, []);

  return (
    <UserContext.Provider value={{ userData, setUserData, loadingUser }}>
      {children}
    </UserContext.Provider>
  );
};