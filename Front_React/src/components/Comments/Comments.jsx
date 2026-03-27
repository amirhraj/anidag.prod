import { useEffect, useState } from "react";
import styles from "./Comments.module.css";
import { jwtDecode } from "jwt-decode"; // исправлено на правильный импорт
import $api from "../../api/auth"; 
import EmojiPicker from 'emoji-picker-react';

const Comments = ({ card }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [user, setUser] = useState(null);
  const [visibleDelete, setVisibleDelete] = useState(null);
  const [userData, setUserData] = useState(null);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [replyTo, setReplyTo] = useState(null); // объект родителя
  const API_URL = import.meta.env.VITE_PROD_API_URL;

  // Проверка пользователя
  useEffect(() => {
    const checkUser = () => {
      const token = localStorage.getItem("access_token");
      const decodedUser = token ? jwtDecode(token) : null;
      setUser(decodedUser || "");
    };
    checkUser();
    const handleStorage = (e) => { if (e.key === "access_token") checkUser(); };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  // Получаем данные пользователя
  useEffect(() => {
    const fetchUserData = async () => {
      if (!user || typeof user !== "object") return;
      try {
        const res = await $api.get(`/user/${user.sub}`);
        setUserData(res.data);
      } catch (e) {
        console.error("Ошибка при получении данных пользователя:", e);
      }
    };
    fetchUserData();
  }, [user]);

  // Получаем комментарии
  const fetchComments = async () => {
    try {
      const res = await $api.get(`/getcomments/${card}`);
      setComments(res.data);
    } catch (e) {
      console.error("Ошибка загрузки комментариев:", e);
    }
  };

  useEffect(() => {
    if (!card) return;
    fetchComments();
    const interval = setInterval(fetchComments, 5000);
    return () => clearInterval(interval);
  }, [card]);

  // Добавление комментария/ответа
  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    try {
      const res = await $api.post(`/comments/${card}`, {
        post_i: card,
        user: user.login,
        text: newComment,
        parent_comment_id: replyTo?.id || null,
      });
      setComments((prev) => [...prev, res.data]);
      setNewComment("");
      setReplyTo(null);
      fetchComments();
    } catch (e) {
      console.error("Ошибка добавления комментария:", e);
    }
  };

  // Удаление
  const handleDeleteComment = async (id) => {
    try {
      await $api.delete(`/deletecomments/${id}`);
      setComments((prev) => prev.filter((c) => c.id !== id));
    } catch (e) {
      console.error("Ошибка удаления комментария:", e);
    }
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString("ru-RU", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    }).replace(".", "");
  };

  // Словарь родительских комментариев
  const parentMap = {};
  comments.forEach(c => { parentMap[c.id] = c; });



const [clickedReplyId, setClickedReplyId] = useState(null);

const handleReplyClick = (commentId, comment) => {
  setClickedReplyId(commentId);
  setReplyTo(comment);

  // Снимаем эффект через 200 мс
  setTimeout(() => setClickedReplyId(null), 200);
};

  return (
    <div className={styles.comments_component}>
      <h3>Комментарии</h3>

      {/* Форма для добавления комментария */}
      <div className={styles.comments_input_component}>
        {replyTo && (
          <div className={styles.reply_info}>
            <span>
              Ответ на <strong>@{replyTo.username}</strong>:{" "}
              {replyTo.content.length > 40
                ? replyTo.content.slice(0, 40) + "..."
                : replyTo.content}
            </span>
            <button onClick={() => setReplyTo(null)}>×</button>
          </div>
        )}
        <textarea
          className={styles.comments_input}
          placeholder={user ? "Ваш комментарий..." : "Вы не авторизованы"}
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          maxLength={1500}
          disabled={!user}
        />
        <div className={styles.controls}>
          <button
            type="button"
            className={styles.emoji_btn}
            onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          >
            😊
          </button>
          <button
            className={styles.comments_btn}
            onClick={handleAddComment}
            disabled={!user}
          >
            {replyTo ? "Ответить" : "Добавить"}
          </button>
        </div>
        {showEmojiPicker && (
          <div className={styles.emoji_picker}>
            <EmojiPicker
              onEmojiClick={(emojiData) =>
                setNewComment((prev) => prev + emojiData.emoji)
              }
              lazyLoadEmojis={true}
            />
          </div>
        )}
      </div>

      {/* Список комментариев */}
      <div className={styles.content_container}>
        {[...comments]
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .map((comment) => {
            const parentComment = comment.parent_comment_id
              ? parentMap[comment.parent_comment_id] || null
              : null;
             

            return (
              <div className={styles.content} key={comment.id}>
                <div className={styles.img_conteiner}>
                  <div className={styles.img}>
                    <img
                      src={comment?.avatars
                        ? `${API_URL}/${comment.avatars.replace(/\\/g, "/")}`
                        : "/profile.png"
                      }
                      alt="Фото профиля"
                      className={styles.image}
                      loading="lazy"
                    />
                  </div>
                </div>

                <div className={styles.comment_heads}>
                  <div className={styles.autor}>{comment.username}</div>
                  <div className={styles.comment_time}>
                    {formatDate(comment.created_at)}
                  </div>
                </div>

                    <div className={styles.comment_text}>

                              {parentComment && (
                                <div className={styles.parentComment_container}>
                                  @{parentComment.username}: {parentComment.content.split("\n")[0].slice(0, 40)}
                                  {parentComment.content.length > 40 ? "..." : ""}{" "}
                                </div>
                              )}

                              <div className={styles.comment_body}>
                                  <div className={styles.comment_text}>{comment.content}</div>
                              </div>
                          
                    </div>

                <div className={styles.options_answers}>
                  <button
                    className={`${styles.more_btn_answers} ${clickedReplyId === comment.id ? styles.clicked : ""}`}
                    onClick={() => handleReplyClick(comment.id, comment)}
                  >
                    Ответить
                  </button>


              {user.login === comment.username && (
                <div className={styles.options}>
                  <button
                    onClick={() =>
                      setVisibleDelete(visibleDelete === comment.id ? null : comment.id)
                    }
                    className={styles.more_btn}
                  >
                    ⋮
                  </button>

                  {visibleDelete === comment.id && (
                    <button
                      className={styles.comments_btn_delete}
                      onClick={() => handleDeleteComment(comment.id)}
                    >
                      Удалить
                    </button>
                 )}
                </div>
              )}
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Comments;
