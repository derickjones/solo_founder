// Come Follow Me utility functions

export interface CFMWeek {
  id: string;
  lesson: string;
  reference: string;
  dates: string;
  weekInfo?: any; // For full lesson data from backend
}

// 2025 Come Follow Me Schedule - Doctrine & Covenants (actual dates from your backend data)
export const CFM_2025_SCHEDULE: CFMWeek[] = [
  { id: 'dc-1-3', lesson: 'Introduction to Doctrine and Covenants', reference: 'Doctrine and Covenants 1–3', dates: 'December 30, 2024–January 5, 2025' },
  { id: 'dc-6-9', lesson: 'The Spirit of Revelation', reference: 'Doctrine and Covenants 6–9', dates: 'January 6–12' },
  { id: 'dc-10-11', lesson: 'Be Not Deceived', reference: 'Doctrine and Covenants 10–11', dates: 'January 13–19' },
  { id: 'dc-18', lesson: 'What Is the Worth of Souls?', reference: 'Doctrine and Covenants 18', dates: 'January 20–26' },
  { id: 'dc-27-28', lesson: 'Listen to Him', reference: 'Doctrine and Covenants 27–28', dates: 'January 27–February 2' },
  { id: 'dc-37-40', lesson: 'Gather My People Together', reference: 'Doctrine and Covenants 37–40', dates: 'February 3–9' },
  { id: 'dc-41-44', lesson: 'The Law of the Church', reference: 'Doctrine and Covenants 41–44', dates: 'February 10–16' },
  { id: 'dc-45-47', lesson: 'Signs of the Times', reference: 'Doctrine and Covenants 45–47', dates: 'February 17–23' },
  { id: 'dc-49-52', lesson: 'The Law of Consecration', reference: 'Doctrine and Covenants 49–52', dates: 'February 24–March 2' },
  { id: 'dc-58-59', lesson: 'Anxiously Engaged', reference: 'Doctrine and Covenants 58–59', dates: 'March 3–9' },
  { id: 'dc-64-66', lesson: 'I, the Lord, Will Forgive', reference: 'Doctrine and Covenants 64–66', dates: 'March 10–16' },
  { id: 'dc-76', lesson: 'Vision of the Three Degrees of Glory', reference: 'Doctrine and Covenants 76', dates: 'March 17–23' },
  { id: 'dc-84', lesson: 'The Power of Godliness', reference: 'Doctrine and Covenants 84', dates: 'March 24–30' },
  { id: 'dc-89', lesson: 'The Word of Wisdom', reference: 'Doctrine and Covenants 89', dates: 'March 31–April 6' },
  { id: 'dc-121-123', lesson: 'Thy Adversity and Thine Afflictions', reference: 'Doctrine and Covenants 121–123', dates: 'November 17–23' },
  { id: 'dc-124', lesson: 'House of Prayer, House of Fasting', reference: 'Doctrine and Covenants 124', dates: 'October 27–November 2' },
  { id: 'dc-125-128', lesson: 'Baptism for the Dead', reference: 'Doctrine and Covenants 125–128', dates: 'November 3–9' },
  { id: 'dc-129-132', lesson: 'Angels and Eternal Marriage', reference: 'Doctrine and Covenants 129–132', dates: 'November 10–16' },
  { id: 'dc-133-134', lesson: 'Prepare for the Second Coming', reference: 'Doctrine and Covenants 133–134', dates: 'November 17–23' },
  { id: 'dc-135-136', lesson: 'He Has Sealed His Mission', reference: 'Doctrine and Covenants 135–136', dates: 'November 24–30' },
  { id: 'dc-137-138', lesson: 'The Vision of the Redemption of the Dead', reference: 'Doctrine and Covenants 137–138', dates: 'December 1–7' },
];

export function getCurrentCFMWeek(): CFMWeek {
  const today = new Date();
  
  // Parse dates and find the current week
  for (const week of CFM_2025_SCHEDULE) {
    if (isDateInWeek(today, week.dates)) {
      return week;
    }
  }
  
  // If no current week found, return the week for December 1-7 (current)
  return CFM_2025_SCHEDULE.find(w => w.id === 'dc-137-138') || CFM_2025_SCHEDULE[0];
}

function isDateInWeek(date: Date, dateRange: string): boolean {
  // Parse date ranges like "November 24–30" or "October 27–November 2"
  const today = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
  
  // Simple check for December dates
  if (dateRange.includes('December')) {
    const currentMonth = date.getMonth(); // 0-11
    if (currentMonth === 11) { // December
      if (dateRange === 'December 1–7' && date.getDate() >= 1 && date.getDate() <= 7) {
        return true;
      }
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
    return CFM_2025_SCHEDULE;
  } catch (error) {
    console.error('Error loading CFM lessons:', error);
    return CFM_2025_SCHEDULE; // Fallback to static data
  }
}

export const CFM_AUDIENCES = [
  { id: 'Adult', label: 'Adult' },
  { id: 'Family', label: 'Family' },
  { id: 'Youth', label: 'Youth' },
  { id: 'Children', label: 'Children' }
];