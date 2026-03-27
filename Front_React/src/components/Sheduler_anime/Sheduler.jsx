
// import { useState, useEffect } from 'react';
// import $api from '../../api/auth';
// import stylesShedule from './shedule.module.css';
// import { ClipLoader } from 'react-spinners';
// import { Link } from 'react-router-dom';

// export default function OvaSection() {
//   const [series, setSeries] = useState([]);
//   const [isExpanded, setIsExpanded] = useState({});
//   const [loading, setLoading] = useState(false);
//   const [skip, setSkip] = useState(0);
//   const [limit] = useState(16); 

//   const MAX_DESCRIPTION_LENGTH = 100;

//   const handleToggle = (index) => {
//     setIsExpanded((prevState) => ({
//       ...prevState,
//       [index]: !prevState[index],
//     }));
//   };

//   useEffect(() => {

//     getAnimeTop();

//   }, []);

//   const weekSchedule = {
//     Понедельник: [],
//     Вторник: [],
//     Среда: [],
//     Четверг: [],
//     Пятница: [],
//     Суббота: [],
//     Воскресенье: []
//   };
  
//   async function getAnimeTop() {
//     try {
//       setLoading(true);
//       const response = await $api.get(`/animes/scheduler/`);
//       // console.log(response.data, "SHEDUL");
  
//       const newSeries = response.data;
//       const updatedSchedule = { ...weekSchedule };
  
//       newSeries.forEach(item => {
//         const weekDay = getWeekDay(item.next_episode_at);
//         if (updatedSchedule[weekDay]) {
//           updatedSchedule[weekDay].push(item);
//         }
//       });
  
//       setSeries(updatedSchedule);
//       setSkip(prevSkip => prevSkip + limit);
//     } catch (error) {
//       console.log(error);
//     } finally {
//       setLoading(false);
//     }
//   }
  



// const getWeekDay = (dateString) => {
//     const days = [ 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница','Суббота', 'Воскресенье'];
//     const date = new Date(dateString);
//     const mondayFirstIndex = (date.getDay() + 6) % 7;

//     return days[mondayFirstIndex];
//     // const date = new Date(dateString);
//     // return days[date.getDay()];
//   };


//   return (
//     <div>
//       <div className={stylesShedule.container}>
               
//                     <div >
                   
//                             {Object.entries(series).map(([day, items], index) => (
//                                 <div key={index} className={stylesShedule.weekDaysWrapers}>
//                                     <h1 className={stylesShedule.h2}>
//                                         {day}
//                                     </h1>
                                   
//                                     <div className={stylesShedule.weekDaysWrapper}>
//                                     {items.map((value, index)=>{
                                      
                                       
//                                                 return (
//                                                     <div key={value.id} className={stylesShedule.card}>
//                                                             <div  className={stylesShedule.card}>
//                                                                 <Link to={`/card/${value.id}/cardOngoing`} className={stylesShedule.link}>
//                                                                     <img src={value.poster_url} alt={value.title} className={stylesShedule.poster} />
//                                                                     <div className={stylesShedule.rating}>
//                                                                                     {value && value.material_data ? value.material_data.shikimori_rating || 0 : 0}
//                                                                     </div>
//                                                                     <h3 className={stylesShedule.title}>{value.title}</h3>
//                                                                     {/* <p className={stylesShedule.description}>{truncatedDescription}</p> */}
//                                                                     {/* {description.length > MAX_DESCRIPTION_LENGTH && ( */}
//                                                                     {/* // <button onClick={() => handleToggle(index)} className={stylesShedule.toggleButton}>
//                                                                     //     {isItemExpanded ? 'Скрыть' : 'Читать больше'}
//                                                                     // </button>
//                                                                     // )} */}
//                                                                 </Link>
//                                                                 </div>
//                                                     </div>
//                                                        );
//                                            })}    
//                                     </div>
//                                 </div>  
//                             ))} 
                        
//                     </div>
//       </div>
   
//     </div>
//   );
// }








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
              {items.map((value, idx) => (
                <div key={`${day}-${value.id}-${idx}`} className={stylesShedule.card}>
                  <Link
                    to={`/card/${value.id}/cardOngoing`}
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
              ))}
            </div>

          </div>
        );
      })}
    </div>
  );
}





