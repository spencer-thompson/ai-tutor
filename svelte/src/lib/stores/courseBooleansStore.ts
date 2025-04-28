import { writable, derived } from 'svelte/store';

// Define the initial state
const initialState: Record<string, boolean> = {};

// Create the writable store
function createCourseBooleanStore() {
    const { subscribe, set, update } = writable<Record<string, boolean>>(initialState);
    
    return {
        subscribe,
        
        // Set a single course boolean
        setCourse: (courseId: string, value: boolean) => update(store => {
            return { ...store, [courseId]: value };
        }),
        
        // Get a single course value
        getCourse: (courseId: string) => {
            let value: boolean = false;
            const unsubscribe = subscribe(store => {
                value = store[courseId] ?? false;
            });
            unsubscribe();
            return value;
        },
        
        // Get all courses
        getAllCourses: () => {
            let courses: Record<string, boolean> = {};
            const unsubscribe = subscribe(store => {
                courses = { ...store };
            });
            unsubscribe();
            return courses;
        }
    };
}

// Export the store
export const courseBooleans = createCourseBooleanStore();
