// Come Follow Me utility functions

export interface CFMWeek {
  id: string;
  lesson: string;
  reference: string;
  dates: string;
  weekInfo?: any; // For full lesson data from backend
}

// 2026 Come Follow Me Schedule - Old Testament (from your backend bundle data)
export const CFM_2026_SCHEDULE: CFMWeek[] = [
  { id: 'ot-week-2', lesson: 'Introduction to the Old Testament', reference: 'Moses 1', dates: 'January 6–12, 2026' },
  { id: 'ot-week-3', lesson: 'The Creation', reference: 'Genesis 1–2; Moses 2–3; Abraham 4–5', dates: 'January 13–19, 2026' },
  { id: 'ot-week-4', lesson: 'The Fall', reference: 'Genesis 3–4; Moses 4–5', dates: 'January 20–26, 2026' },
  { id: 'ot-week-5', lesson: 'Noah and the Flood', reference: 'Genesis 6–9; Moses 8', dates: 'January 27–February 2, 2026' },
  { id: 'ot-week-6', lesson: 'The Abrahamic Covenant', reference: 'Genesis 12–17; Abraham 1–2', dates: 'February 3–9, 2026' },
  { id: 'ot-week-7', lesson: 'Isaac and Rebekah', reference: 'Genesis 24–28', dates: 'February 10–16, 2026' },
  { id: 'ot-week-8', lesson: 'Jacob and Esau', reference: 'Genesis 25–33', dates: 'February 17–23, 2026' },
  { id: 'ot-week-9', lesson: 'Joseph in Egypt', reference: 'Genesis 37–50', dates: 'February 24–March 2, 2026' },
  { id: 'ot-week-10', lesson: 'Moses and the Exodus', reference: 'Exodus 1–6', dates: 'March 3–9, 2026' },
  { id: 'ot-week-11', lesson: 'The Passover and Exodus', reference: 'Exodus 7–13', dates: 'March 10–16, 2026' },
  { id: 'ot-week-12', lesson: 'The Red Sea and Mount Sinai', reference: 'Exodus 14–20', dates: 'March 17–23, 2026' },
  { id: 'ot-week-13', lesson: 'The Ten Commandments', reference: 'Exodus 19–20; 32–34', dates: 'March 24–30, 2026' },
  { id: 'ot-week-14', lesson: 'The Tabernacle', reference: 'Exodus 25–30; 35–40', dates: 'March 31–April 6, 2026' },
  { id: 'ot-week-15', lesson: 'The Law of Moses', reference: 'Leviticus 1; 16; 19; 26', dates: 'April 7–13, 2026' },
  { id: 'ot-week-16', lesson: 'In the Wilderness', reference: 'Numbers 11–14; 21–24', dates: 'April 14–20, 2026' },
  { id: 'ot-week-17', lesson: 'Deuteronomy', reference: 'Deuteronomy 6–8; 30–32', dates: 'April 21–27, 2026' },
  { id: 'ot-week-18', lesson: 'The Promised Land', reference: 'Numbers 13–14; Deuteronomy 1; 8; 32–34', dates: 'April 28–May 4, 2026' },
  { id: 'ot-week-19', lesson: 'Be Strong and of Good Courage', reference: 'Joshua 1–8; 23–24', dates: 'May 5–11, 2026' },
  { id: 'ot-week-20', lesson: 'Choose You This Day', reference: 'Joshua 1–8', dates: 'May 12–18, 2026' },
  { id: 'ot-week-21', lesson: 'The Lord Raised Up Judges', reference: 'Judges 2–4; 6–7; 13–16', dates: 'May 19–25, 2026' },
  { id: 'ot-week-22', lesson: 'Ruth and Samuel', reference: 'Ruth; 1 Samuel 1–3', dates: 'May 26–June 1, 2026' },
  { id: 'ot-week-23', lesson: 'We Will Have a King', reference: '1 Samuel 8–10; 13; 15–17', dates: 'June 2–8, 2026' },
  { id: 'ot-week-24', lesson: 'David and Goliath', reference: '1 Samuel 16–20', dates: 'June 9–15, 2026' },
  { id: 'ot-week-25', lesson: 'How Are the Mighty Fallen', reference: '2 Samuel 11–12; 1 Kings 1–2', dates: 'June 16–22, 2026' },
  { id: 'ot-week-26', lesson: 'The Reign of Solomon', reference: '1 Kings 3; 5–11', dates: 'June 23–29, 2026' },
  { id: 'ot-week-27', lesson: 'Elijah the Prophet', reference: '1 Kings 17–19', dates: 'June 30–July 6, 2026' },
  { id: 'ot-week-28', lesson: 'Elisha the Prophet', reference: '2 Kings 2–7; 13', dates: 'July 7–13, 2026' },
  { id: 'ot-week-29', lesson: 'The Fall of Israel and Judah', reference: '2 Kings 14–25', dates: 'July 14–20, 2026' },
  { id: 'ot-week-30', lesson: 'Return from Captivity', reference: '1 Chronicles 17; 21–22; 28–29; 2 Chronicles 20; Ezra 1; 3; 6–7', dates: 'July 21–27, 2026' },
  { id: 'ot-week-31', lesson: 'Ezra and Nehemiah', reference: 'Ezra 1; 3; 6–7; Nehemiah 1–2; 4; 6; 8', dates: 'July 28–August 3, 2026' },
  { id: 'ot-week-32', lesson: 'Job', reference: 'Job 1–3; 13–14; 19; 27; 42', dates: 'August 4–10, 2026' },
  { id: 'ot-week-33', lesson: 'The Lord Is My Shepherd', reference: 'Psalm 23', dates: 'August 11–17, 2026' },
  { id: 'ot-week-34', lesson: 'Psalms', reference: 'Psalms 1; 2; 22; 23; 24', dates: 'August 18–24, 2026' },
  { id: 'ot-week-35', lesson: 'Proverbs', reference: 'Proverbs 1; 15; 31', dates: 'August 25–31, 2026' },
  { id: 'ot-week-36', lesson: 'Ecclesiastes', reference: 'Ecclesiastes 1–3; 12', dates: 'September 1–7, 2026' },
  { id: 'ot-week-37', lesson: 'Isaiah Sees the Lord', reference: 'Isaiah 1–6', dates: 'September 8–14, 2026' },
  { id: 'ot-week-38', lesson: 'A Virgin Shall Conceive', reference: 'Isaiah 7–11; 53', dates: 'September 15–21, 2026' },
  { id: 'ot-week-39', lesson: 'Look unto Me and Be Ye Saved', reference: 'Isaiah 40–49', dates: 'September 22–28, 2026' },
  { id: 'ot-week-40', lesson: 'Beside Me There Is No Savior', reference: 'Isaiah 50–66', dates: 'September 29–October 5, 2026' },
  { id: 'ot-week-41', lesson: 'Mine Anger Is Not Forever', reference: 'Jeremiah 1–3; 7; 16–17; 20', dates: 'October 6–12, 2026' },
  { id: 'ot-week-42', lesson: 'A New Heart and a New Covenant', reference: 'Jeremiah 31; 33; Lamentations 3; Ezekiel 18; 34; 36–37', dates: 'October 13–19, 2026' },
  { id: 'ot-week-43', lesson: 'I Will Write It in Their Hearts', reference: 'Ezekiel 1–3; 18; 34; 36–37', dates: 'October 20–26, 2026' },
  { id: 'ot-week-44', lesson: 'Visions and Dreams of Daniel', reference: 'Daniel 1–3; 6', dates: 'October 27–November 2, 2026' },
  { id: 'ot-week-45', lesson: 'When the Lord Shall Return', reference: 'Daniel 2; 7–12', dates: 'November 3–9, 2026' },
  { id: 'ot-week-46', lesson: 'I Will Heal Their Backsliding', reference: 'Hosea 1–3; 11; 13–14', dates: 'November 10–16, 2026' },
  { id: 'ot-week-47', lesson: 'Prepare to Meet Thy God', reference: 'Joel; Amos; Obadiah', dates: 'November 17–23, 2026' },
  { id: 'ot-week-48', lesson: 'Who Is a God Like unto Thee?', reference: 'Jonah; Micah', dates: 'November 24–30, 2026' },
  { id: 'ot-week-49', lesson: 'The Lord Is in His Holy Temple', reference: 'Nahum; Habakkuk; Zephaniah', dates: 'December 1–7, 2026' },
  { id: 'ot-week-50', lesson: 'Consider Your Ways', reference: 'Haggai; Zechariah 1–3; 12–14; Malachi', dates: 'December 8–14, 2026' },
  { id: 'ot-week-51', lesson: 'Will a Man Rob God?', reference: 'Malachi', dates: 'December 15–21, 2026' },
  { id: 'ot-week-52', lesson: 'The Coming of Elijah', reference: 'Malachi 3–4', dates: 'December 22–28, 2026' },
];

export function getCurrentCFMWeek(): CFMWeek {
  const today = new Date();
  
  // Parse dates and find the current week
  for (const week of CFM_2026_SCHEDULE) {
    if (isDateInWeek(today, week.dates)) {
      return week;
    }
  }
  
  // If no current week found, return the week for January 13-19 (current)
  return CFM_2026_SCHEDULE.find(w => w.id === 'ot-week-3') || CFM_2026_SCHEDULE[0];
}

function isDateInWeek(date: Date, dateRange: string): boolean {
  // Parse date ranges like "January 13–19, 2026" or "January 27–February 2, 2026"
  const today = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
  
  // For now, return true for January 13-19, 2026 (Genesis 1-2 week) as current week
  // This can be enhanced later with proper date parsing
  if (dateRange === 'January 13–19, 2026') {
    const currentMonth = date.getMonth(); // 0-11 (0 = January)
    const currentDate = date.getDate();
    if (currentMonth === 0 && currentDate >= 13 && currentDate <= 19) { // January 13-19
      return true;
    }
  }
  
  return false;
}

export function formatCFMWeekDisplay(week: CFMWeek): string {
  return `${week.dates}: ${week.lesson}`;
}

// Function to load CFM lessons from your backend API
export async function loadCFMLessonsFromAPI(): Promise<CFMWeek[]> {
  try {
    // TODO: Replace with actual API call when you implement the CFM endpoints
    // const response = await fetch('/api/cfm/lessons?year=2025');
    // const data = await response.json();
    // 
    // Transform your backend data structure to CFMWeek interface:
    // return data.map((lesson: any) => ({
    //   id: lesson.lesson_title.toLowerCase().replace(/\s+/g, '-'),
    //   lesson: lesson.lesson_title,
    //   reference: lesson.lesson_title,
    //   dates: lesson.week_info, // Extract dates from your week_info field
    //   weekInfo: lesson // Store full lesson data
    // }));
    
    // For now, return the static schedule
    return CFM_2026_SCHEDULE;
  } catch (error) {
    console.error('Error loading CFM lessons:', error);
    return CFM_2026_SCHEDULE; // Fallback to static data
  }
}

export const CFM_AUDIENCES = [
  { id: 'Family', label: 'Family' },
  { id: 'Adult', label: 'Adult' },
  { id: 'Youth', label: 'Youth' },
  { id: 'Children', label: 'Children' }
];