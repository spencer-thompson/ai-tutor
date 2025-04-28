import {userData} from '$lib/stores/userDataStore';

export async function load({ data }) {
    try {
        const response = await fetch('https://api.aitutor.live/user', {
            headers: {
                'AITUTOR-API-KEY': data.apiKey,
                'Authorization': `Bearer ${data.token}`,
                // 'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        
        const apiData = await response.json();
        await storeData(apiData)
        
        return {
            ...data,
            apiData
        };
    } catch (error) {
        return {
            ...data,
            error: error.message
        };
    }
}

async function storeData(apiData) {
   console.log(apiData);
   console.log(apiData.role);
   
   userData.update(currentData => {
     return {...apiData };
   });
}
