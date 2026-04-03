import { useState, useEffect, useMemo } from "react";
import $api from "../../api/auth";
import stylesShedule from "./shedule.module.css";
import { ClipLoader } from "react-spinners";
import { Link } from "react-router-dom";

export default function OvaSection() {
  const weekSchedule = useMemo(
    () => ({
      Понедельник: [],
      Вторник: [],
      Среда: [],
      Четверг: [],
      Пятница: [],
      Суббота: [],
      Воскресенье: [],
    }),
    []
  );

  const [series, setSeries] = useState(weekSchedule);
  const [loading, setLoading] = useState(false);

  const [openDays, setOpenDays] = useState({
    Понедельник: true,
    Вторник: false,
    Среда: false,
    Четверг: false,
    Пятница: false,
    Суббота: false,
    Воскресенье: false,
  });

  const toggleDay = (day) => {
    setOpenDays((prev) => {
      const next = {};
      Object.keys(prev).forEach((k) => (next[k] = false));
      next[day] = !prev[day];
      return next;
    });
  };

  const getWeekDay = (dateString) => {
    const days = [
      "Понедельник",
      "Вторник",
      "Среда",
      "Четверг",
      "Пятница",
      "Суббота",
      "Воскресенье",
    ];
    const date = new Date(dateString);
    const mondayFirstIndex = (date.getDay() + 6) % 7;
    return days[mondayFirstIndex];
  };

  async function getAnimeTop() {
    try {
      setLoading(true);
      const response = await $api.get(`/animes/scheduler/`);

      const newSeries = response.data;
      const updatedSchedule = { ...weekSchedule };

      newSeries.forEach((item) => {
        const weekDay = getWeekDay(item.next_episode_at);
        if (updatedSchedule[weekDay]) updatedSchedule[weekDay].push(item);
      });

      setSeries(updatedSchedule);
    } catch (error) {
      console.log(
        "Scheduler error:",
        error?.response?.status,
        error?.response?.data || error.message
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getAnimeTop();
  }, []);



  const getTodayRuDay = () => {
  const days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
  ];
  // getDay(): 0=вс,1=пн..6=сб → делаем 0=пн..6=вс
  const idx = (new Date().getDay() + 6) % 7;
  return days[idx];
};

const makeOpenDays = (openDay) => ({
  Понедельник: openDay === "Понедельник",
  Вторник: openDay === "Вторник",
  Среда: openDay === "Среда",
  Четверг: openDay === "Четверг",
  Пятница: openDay === "Пятница",
  Суббота: openDay === "Суббота",
  Воскресенье: openDay === "Воскресенье",
});

useEffect(() => {
  setOpenDays(makeOpenDays(getTodayRuDay()));
}, []);


  return (
    <div className={stylesShedule.container}>
      {loading && (
        <div style={{ display: "flex", justifyContent: "center", padding: 20 }}>
          <ClipLoader />
        </div>
      )}

      {Object.entries(series).map(([day, items]) => {
        const isOpen = !!openDays[day];

        return (
          <div key={day} className={stylesShedule.weekDaysWrapers}>
          <button className={stylesShedule.dayHeader} onClick={() => toggleDay(day)}>
            <span className={stylesShedule.dayTitle}>{day}</span>
            <span className={`${stylesShedule.chevron} ${isOpen ? stylesShedule.rot : ""}`}>
              ▼
            </span>
          </button>
            <div
              className={`${stylesShedule.weekDaysWrapper} ${
                isOpen ? stylesShedule.open : stylesShedule.closed
              }`}
            >
              {/* {items.map((value, idx) => (
                <div key={`${day}-${value.id}-${idx}`} className={stylesShedule.card}>
                  <Link
                    to={`/anime/${value.id}/animeongoing`}
                    className={stylesShedule.link}
                  >
                    <img
                      src={value.poster_url}
                      alt={value.title}
                      className={stylesShedule.poster}
                    />
                    <div className={stylesShedule.rating}>
                      {value?.material_data?.shikimori_rating || 0}
                    </div>
                    <h3 className={stylesShedule.title}>{value.title}</h3>
                  </Link>
                </div>
              ))} */}
              {items.map((value, idx) => {
                    const makeSlug = (text = "") => {
                      return text
                        .toLowerCase()
                        .trim()
                        .replace(/[^\p{L}\p{N}\s-]/gu, "")
                        .replace(/\s+/g, "-")
                        .replace(/-+/g, "-");
                    };

                    const titleForSlug =
                      value.title_orig ??
                      value.title ??
                      value.russian_name ??
                      "anime";

                    const seoPart = `${makeSlug(titleForSlug)}-${value.id}`;

                    return (
                      <div key={`${day}-${value.id}-${idx}`} className={stylesShedule.card}>
                        <Link
                          to={`/anime/${seoPart}/animeongoing`}
                          className={stylesShedule.link}
                        >
                          <img
                            src={value.poster_url}
                            alt={value.title}
                            className={stylesShedule.poster}
                          />
                          <div className={stylesShedule.rating}>
                            {value?.material_data?.shikimori_rating || 0}
                          </div>
                          <h3 className={stylesShedule.title}>{value.title}</h3>
                        </Link>
                      </div>
                    );
                  })}
            </div>

          </div>
        );
      })}
    </div>
  );
}





