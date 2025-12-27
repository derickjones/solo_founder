// Come Follow Me utility functions

export interface CFMWeek {
  id: string;
  lesson: string;
  reference: string;
  dates: string;
  weekInfo?: any; // For full lesson data from backend
}

// 2026 Come Follow Me Schedule - Complete 52 weeks from enhanced bundles
export const CFM_2026_SCHEDULE: CFMWeek[] = [
  { id: 'cfm-2026-week-01', lesson: 'Week 1: December 29–January 4 - Introduction to the Old Testament', reference: '', dates: 'December 29–January 4' },
  { id: 'cfm-2026-week-02', lesson: 'Week 2: January 5–11 - Moses 1; Abraham 3', reference: 'Moses 1; Abraham 3', dates: 'January 5–11' },
  { id: 'cfm-2026-week-03', lesson: 'Week 3: January 12–18 - Genesis 1–2; Moses 2–3; Abraham 4–5', reference: 'Genesis 1–2; Moses 2–3; Abraham 4–5', dates: 'January 12–18' },
  { id: 'cfm-2026-week-04', lesson: 'Week 4: January 19–25 - Genesis 3–4; Moses 4–5', reference: 'Genesis 3–4; Moses 4–5', dates: 'January 19–25' },
  { id: 'cfm-2026-week-05', lesson: 'Week 5: January 26–February 1 - Genesis 5; Moses 6', reference: 'Genesis 5; Moses 6', dates: 'January 26–February 1' },
  { id: 'cfm-2026-week-06', lesson: 'Week 6: February 2–8 - Moses 7', reference: 'Moses 7', dates: 'February 2–8' },
  { id: 'cfm-2026-week-07', lesson: 'Week 7: February 9–15 - Genesis 6–11; Moses 8', reference: 'Genesis 6–11; Moses 8', dates: 'February 9–15' },
  { id: 'cfm-2026-week-08', lesson: 'Week 8: February 16–22 - Genesis 12–17; Abraham 1–2', reference: 'Genesis 12–17; Abraham 1–2', dates: 'February 16–22' },
  { id: 'cfm-2026-week-09', lesson: 'Week 9: February 23–March 1 - Genesis 18–23', reference: 'Genesis 18–23', dates: 'February 23–March 1' },
  { id: 'cfm-2026-week-10', lesson: 'Week 10: March 2–8 - Genesis 24–33', reference: 'Genesis 24–33', dates: 'March 2–8' },
  { id: 'cfm-2026-week-11', lesson: 'Week 11: March 9–15 - Genesis 37–41', reference: 'Genesis 37–41', dates: 'March 9–15' },
  { id: 'cfm-2026-week-12', lesson: 'Week 12: March 16–22 - Genesis 42–50', reference: 'Genesis 42–50', dates: 'March 16–22' },
  { id: 'cfm-2026-week-13', lesson: 'Week 13: March 23–29 - Exodus 1–6', reference: 'Exodus 1–6', dates: 'March 23–29' },
  { id: 'cfm-2026-week-14', lesson: 'Week 14: March 30–April 5 - Easter', reference: '', dates: 'March 30–April 5' },
  { id: 'cfm-2026-week-15', lesson: 'Week 15: April 6–12 - Exodus 7–13', reference: 'Exodus 7–13', dates: 'April 6–12' },
  { id: 'cfm-2026-week-16', lesson: 'Week 16: April 13–19 - Exodus 14–18', reference: 'Exodus 14–18', dates: 'April 13–19' },
  { id: 'cfm-2026-week-17', lesson: 'Week 17: April 20–26 - Exodus 19–20; 24; 31–34', reference: 'Exodus 19–20; 24; 31–34', dates: 'April 20–26' },
  { id: 'cfm-2026-week-18', lesson: 'Week 18: April 27–May 3 - Exodus 35–40; Leviticus 1; 4; 16; 19', reference: 'Exodus 35–40; Leviticus 1; 4; 16; 19', dates: 'April 27–May 3' },
  { id: 'cfm-2026-week-19', lesson: 'Week 19: May 4–10 - Numbers 11–14; 20–24; 27', reference: 'Numbers 11–14; 20–24; 27', dates: 'May 4–10' },
  { id: 'cfm-2026-week-20', lesson: 'Week 20: May 11–17 - Deuteronomy 6–8; 15; 18; 29–30; 34', reference: 'Deuteronomy 6–8; 15; 18; 29–30; 34', dates: 'May 11–17' },
  { id: 'cfm-2026-week-21', lesson: 'Week 21: May 18–24 - Joshua 1–8; 23–24', reference: 'Joshua 1–8; 23–24', dates: 'May 18–24' },
  { id: 'cfm-2026-week-22', lesson: 'Week 22: May 25–31 - Judges 2–4; 6–8; 13–16', reference: 'Judges 2–4; 6–8; 13–16', dates: 'May 25–31' },
  { id: 'cfm-2026-week-23', lesson: 'Week 23: June 1–7 - Ruth; 1 Samuel 1–7', reference: 'Ruth; 1 Samuel 1–7', dates: 'June 1–7' },
  { id: 'cfm-2026-week-24', lesson: 'Week 24: June 8–14 - 1 Samuel 8–10; 13; 15–16', reference: '1 Samuel 8–10; 13; 15–16', dates: 'June 8–14' },
  { id: 'cfm-2026-week-25', lesson: 'Week 25: June 15–21 - 1 Samuel 17–18; 24–26; 2 Samuel 5–7', reference: '1 Samuel 17–18; 24–26; 2 Samuel 5–7', dates: 'June 15–21' },
  { id: 'cfm-2026-week-26', lesson: 'Week 26: June 22–28 - 2 Samuel 11–12; 1 Kings 3; 6–9; 11', reference: '2 Samuel 11–12; 1 Kings 3; 6–9; 11', dates: 'June 22–28' },
  { id: 'cfm-2026-week-27', lesson: 'Week 27: June 29–July 5 - 1 Kings 12–13; 17–22', reference: '1 Kings 12–13; 17–22', dates: 'June 29–July 5' },
  { id: 'cfm-2026-week-28', lesson: 'Week 28: July 6–12 - 2 Kings 2–7', reference: '2 Kings 2–7', dates: 'July 6–12' },
  { id: 'cfm-2026-week-29', lesson: 'Week 29: July 13–19 - 2 Kings 16–25', reference: '2 Kings 16–25', dates: 'July 13–19' },
  { id: 'cfm-2026-week-30', lesson: 'Week 30: July 20–26 - 2 Chronicles 14–20; 26; 30', reference: '2 Chronicles 14–20; 26; 30', dates: 'July 20–26' },
  { id: 'cfm-2026-week-31', lesson: 'Week 31: July 27–August 2 - Ezra 1; 3–7; Nehemiah 2; 4–6; 8', reference: 'Ezra 1; 3–7; Nehemiah 2; 4–6; 8', dates: 'July 27–August 2' },
  { id: 'cfm-2026-week-32', lesson: 'Week 32: August 3–9 - Esther', reference: 'Esther', dates: 'August 3–9' },
  { id: 'cfm-2026-week-33', lesson: 'Week 33: August 10–16 - Job 1–3; 12–14; 19; 21–24; 38–40; 42', reference: 'Job 1–3; 12–14; 19; 21–24; 38–40; 42', dates: 'August 10–16' },
  { id: 'cfm-2026-week-34', lesson: 'Week 34: August 17–23 - Psalms 1–2; 8; 19–33; 40; 46', reference: 'Psalms 1–2; 8; 19–33; 40; 46', dates: 'August 17–23' },
  { id: 'cfm-2026-week-35', lesson: 'Week 35: August 24–30 - Psalms 49–51; 61–66; 69–72; 77–78; 85–86', reference: 'Psalms 49–51; 61–66; 69–72; 77–78; 85–86', dates: 'August 24–30' },
  { id: 'cfm-2026-week-36', lesson: 'Week 36: August 31–September 6 - Psalms 102–103; 110; 116–119; 127–128; 135–139; 146–150', reference: 'Psalms 102–103; 110; 116–119; 127–128; 135–139; 146–150', dates: 'August 31–September 6' },
  { id: 'cfm-2026-week-37', lesson: 'Week 37: September 7–13 - Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12', reference: 'Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12', dates: 'September 7–13' },
  { id: 'cfm-2026-week-38', lesson: 'Week 38: September 14–20 - Isaiah 1–12', reference: 'Isaiah 1–12', dates: 'September 14–20' },
  { id: 'cfm-2026-week-39', lesson: 'Week 39: September 21–27 - Isaiah 13–14; 22; 24–30; 35', reference: 'Isaiah 13–14; 22; 24–30; 35', dates: 'September 21–27' },
  { id: 'cfm-2026-week-40', lesson: 'Week 40: September 28–October 4 - Isaiah 40–49', reference: 'Isaiah 40–49', dates: 'September 28–October 4' },
  { id: 'cfm-2026-week-41', lesson: 'Week 41: October 5–11 - Isaiah 50–57', reference: 'Isaiah 50–57', dates: 'October 5–11' },
  { id: 'cfm-2026-week-42', lesson: 'Week 42: October 12–18 - Isaiah 58–66', reference: 'Isaiah 58–66', dates: 'October 12–18' },
  { id: 'cfm-2026-week-43', lesson: 'Week 43: October 19–25 - Jeremiah 1–3; 7; 16–18; 20', reference: 'Jeremiah 1–3; 7; 16–18; 20', dates: 'October 19–25' },
  { id: 'cfm-2026-week-44', lesson: 'Week 44: October 26–November 1 - Jeremiah 31–33; 36–39; Lamentations 1; 3', reference: 'Jeremiah 31–33; 36–39; Lamentations 1; 3', dates: 'October 26–November 1' },
  { id: 'cfm-2026-week-45', lesson: 'Week 45: November 2–8 - Ezekiel 1–3; 33–34; 36–37; 47', reference: 'Ezekiel 1–3; 33–34; 36–37; 47', dates: 'November 2–8' },
  { id: 'cfm-2026-week-46', lesson: 'Week 46: November 9–15 - Daniel 1–7', reference: 'Daniel 1–7', dates: 'November 9–15' },
  { id: 'cfm-2026-week-47', lesson: 'Week 47: November 16–22 - Hosea 1–6; 10–14; Joel', reference: 'Hosea 1–6; 10–14; Joel', dates: 'November 16–22' },
  { id: 'cfm-2026-week-48', lesson: 'Week 48: November 23–29 - Amos; Obadiah; Jonah', reference: 'Amos; Obadiah; Jonah', dates: 'November 23–29' },
  { id: 'cfm-2026-week-49', lesson: 'Week 49: November 30–December 6 - Micah; Nahum; Habakkuk; Zephaniah', reference: 'Micah; Nahum; Habakkuk; Zephaniah', dates: 'November 30–December 6' },
  { id: 'cfm-2026-week-50', lesson: 'Week 50: December 7–13 - Haggai 1–2; Zechariah 1–4; 7–14', reference: 'Haggai 1–2; Zechariah 1–4; 7–14', dates: 'December 7–13' },
  { id: 'cfm-2026-week-51', lesson: 'Week 51: December 14–20 - Malachi', reference: 'Malachi', dates: 'December 14–20' },
  { id: 'cfm-2026-week-52', lesson: 'Week 52: December 21–27 - Christmas', reference: '', dates: 'December 21–27' },
];

export function getCurrentCFMWeek(): CFMWeek {
  const today = new Date();
  const currentDate = today.getDate();
  const currentMonth = today.getMonth() + 1; // 1-12
  const currentYear = today.getFullYear();
  
  // CFM 2026 starts Dec 29, 2025 (Week 1) and runs through Dec 27, 2026 (Week 52)
  // Each week starts on Sunday
  
  // Week 1: Dec 29, 2025 - Jan 4, 2026
  const week1Start = new Date(2025, 11, 29); // Dec 29, 2025
  
  // Calculate days since Week 1 started
  const diffTime = today.getTime() - week1Start.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  // Calculate week number (0-indexed, then add 1)
  let weekNumber = Math.floor(diffDays / 7) + 1;
  
  // Clamp to valid range (1-52)
  weekNumber = Math.max(1, Math.min(52, weekNumber));
  
  // If we're before Week 1 starts (before Dec 29, 2025), show Week 1
  if (diffDays < 0) {
    weekNumber = 1;
  }
  
  return CFM_2026_SCHEDULE[weekNumber - 1];
}

export function formatCFMWeekDisplay(week: CFMWeek): string {
  return week.lesson;
}

export const CFM_AUDIENCES = [
  { id: 'Family', label: 'Family' },
  { id: 'Adult', label: 'Adult' },
  { id: 'Youth', label: 'Youth' },
  { id: 'Children', label: 'Children' }
];
