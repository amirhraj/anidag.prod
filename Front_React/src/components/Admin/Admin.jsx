import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // используем :type в URL
import { ClipLoader } from 'react-spinners';
import $api from '../../api/auth';
import s from './admin.module.css';
import { jwtDecode } from 'jwt-decode';
import { Link, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';




export default function AdminPage() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [accessToken, setAccessToken] = useState(null);
    const [period, setPeriod] = useState('week'); 
    const [id, setId] = useState("");
    const [message, setMessage] = useState("");

    const [stats, setStats] = useState([]);
    const [titles, setTitles] = useState([]);
    const [loading, setLoading] = useState(true);

        useEffect(() => {
        if (isLoggedIn) {
            $api.get(`/admin/stats?period=${period}`)
            .then((res) => {
                setStats(res.data);
            })
            .catch((err) => {
                console.error("Ошибка загрузки статистики:", err);
            });
        }
        }, [isLoggedIn, period]);


const handleSubmitModal = async (event) => {
  event.preventDefault();

  try {
    const response = await $api.post(
      '/adminlogin',
      { email, password },
      { headers: { 'Content-Type': 'application/json' } }
    );

    // Токен и данные
    const accessToken = response.data.access_token;
    const tokenType = response.data.token_type;
    const userData = {
      user_id: response.data.user_id,
      email: response.data.email,
      login: response.data.login,
      avatar_url: response.data.avatar_url,
      role: response.data.role,
    };

    // Сохраняем токен и данные в localStorage
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('token_type', tokenType);
    localStorage.setItem('admin_data', JSON.stringify(userData));

    // Декодирование токена (если нужно)
    const tokenPayload = jwtDecode(accessToken); // например, id, email, role

    // setUserData(userData) — если ты используешь useContext или useState
    setIsLoggedIn(true);
    setAccessToken(accessToken);

    // Навигация на админку или нужную страницу
    if (response.status === 200) {
     setIsLoggedIn(true);
    }
  } catch (error) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('admin_data');
    
    setIsLoggedIn(false);
    navigate('/');

    const detail = error?.response?.data?.detail;
    let message = 'Произошла ошибка';

    if (typeof detail === 'string') {
      message = detail;
    } else if (Array.isArray(detail) && detail[0]?.msg) {
      message = detail[0].msg;
    } else if (typeof detail === 'object' && detail?.msg) {
      message = detail.msg;
    }

    setError(message);
  }
};



  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!id) {
      setMessage("Введите ID тайтла");
      return;
    }

    try {
      // достаём роль из localStorage
      const adminData = JSON.parse(localStorage.getItem("admin_data"));
      if (!adminData || adminData.role !== "Admin") {
        setMessage("❌ У вас нет прав для удаления тайтлов");
        return;
      }

      // если роль подходит — отправляем запрос
      const response = await $api.delete(`/anime/${id}`);
      setMessage(`✅ Тайтл с ID ${id} успешно удалён`);
      setId(""); // очистим поле
    } catch (error) {
      console.error("Ошибка при удалении:", error);
      setMessage("Ошибка при удалении тайтла ❌");
    }
  };



  useEffect(() => {
  const fetchTopTitles = async () => {
    try {
      setLoading(true);
      const response = await $api.get("/top-viewed"); // ваш эндпоинт
      setTitles(response.data); // ожидаем массив объектов { anime_id, title, views_count }
    } catch (err) {
      console.error(err);
      setError("Ошибка при загрузке данных");
    } finally {
      setLoading(false);
    }
  };

  // Проверяем роль перед запросом
  const adminData = JSON.parse(localStorage.getItem("admin_data"));
  if (!adminData || adminData.role !== "Admin") {
    setMessage("❌ У вас нет прав для просмотра топа");
    return; // выходим, запрос не выполняется
  }

  fetchTopTitles(); // вызываем только если роль "Admin"
}, []);


    return (
        <div className={s.mainAdminBlock}>
            {accessToken ? (
               <div>
                <h1>Добро пожаловать</h1>
                    <h2>Просмотры за последнюю неделю</h2>
                    <div style={{ marginBottom: '16px' }}>
                    <label htmlFor="period">Период: </label>
                            <select id="period" value={period} onChange={(e) => setPeriod(e.target.value)}>
                                <option value="week">Неделя</option>
                                <option value="month">Месяц</option>
                                <option value="halfyear">Полгода</option>
                                <option value="year">Год</option>
                            </select>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={stats}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="views" stroke="#8884d8" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>


                  <div>
                          <form onSubmit={handleSubmit}>
                            <label htmlFor="animeId">Введите ID тайтла:</label>
                            <input
                              id="animeId"
                              type="text"
                              value={id}
                              onChange={(e) => setId(e.target.value)}
                              placeholder="Например: 123"
                              style={{ marginLeft: "10px", padding: "5px" }}
                            />
                            <button type="submit" style={{ marginLeft: "10px", padding: "5px 10px" }}>
                              Удалить
                            </button>
                          </form>

                          {message && <p >{message}</p>}
                </div>



                  <div>
                     <h2>Топ 10 самых просматриваемых тайтлов</h2>
                        <ul>
                          {titles.map((t, index) => (
                            <li key={t.anime_id}>
                              {index + 1}. {t.title} — {t.views_count} просмотров
                            </li>
                          ))}
                        </ul>
                   </div>

               </div>




            ) : (
                <div>
                    <h2>Вход в админку</h2>
                    <input
                        type="text"
                        placeholder="Email"
                        value={email}
                         onChange={(e) => setEmail(e.target.value)}
                    />
                    <br />
                    <input
                        type="password"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <br />
                    <button onClick={handleSubmitModal}>Войти</button>
                </div>
            )}
        </div>
    );
}

