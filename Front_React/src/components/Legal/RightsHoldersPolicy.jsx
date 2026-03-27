import { useEffect } from 'react';
import stylesPolicy from './/RightsHoldersPolicy.module.css';



export default function RightsHoldersPolicy() {

 useEffect(() => {
    document.title = "Для правообладателей";

    const setMeta = (name, content, isProperty = false) => {
      const selector = isProperty
        ? `meta[property="${name}"]`
        : `meta[name="${name}"]`;

      let meta = document.querySelector(selector);
      if (!meta) {
        meta = document.createElement("meta");
        isProperty
          ? meta.setAttribute("property", name)
          : meta.setAttribute("name", name);
        document.head.appendChild(meta);
      }
      meta.setAttribute("content", content);
    };

    setMeta("description", "Anidag - Смотри аниме онлайн");
    setMeta("og:title", "Anidag - Смотри аниме онлайн", true);
  }, []);

  return (
    <div>
              <title>Для правообладателей</title>
              <meta name="description" content="Anidag (Анидаг) - Смотри аниме онлайн" />
              <meta property="og:title" content="Anidag (Анидаг) - Смотри аниме онлайн" />

      <div className={stylesPolicy.container}>
            <div className={stylesPolicy.content_conteiner}> 
                <p>
                    Руководство портала действует согласно законам Российской Федерации и следует всем необходимым процедурам добровольного урегулирования споров об интеллектуальных правах в соответствии 
                    со ст. 15.7 ФЗ-149 «Об информации, информационных технологиях и о защите информации».
                </p> 
                <p>
                        Если вы сотрудник государственных органов и обнаружили, что на сайте размещен контент, 
                    противоречащий законом Российской Федерации, или, контент, на основании которого вынесено определение и приняты меры, направленные на обеспечение защиты авторских и (или) смежных прав, 
                    то просим в кротчайшие сроки обратиться по электронному адресу  <span className={stylesPolicy.email}>anidaghd@gmail.com
                        </span> и указать ссылки с нашего портала, где размещен запрещенный материал.
                </p>
            </div>
      </div>
    </div>
  );
}
