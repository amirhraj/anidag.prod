export function formatDate(dateString) {
    if (!dateString) return '—';
  
    try {
      const [datePart] = dateString.split('T'); // отрезаем время
      const [year, month, day] = datePart.split('-'); // YYYY-MM-DD → [YYYY, MM, DD]
      return `${day}.${month}.${year}`; // форматируем
    } catch {
      return '—';
    }
  }