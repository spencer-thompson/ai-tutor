import { join } from 'path'
import type { Config } from 'tailwindcss'
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import { skeleton } from '@skeletonlabs/tw-plugin'

export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}', join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}')],
	theme: {
		extend: {
      opacity: {
        'gray-rgba': 'rgba(33,33,33,.33)',
      },
    },
	},
	plugins: [
		forms,
		typography,
		skeleton({
			themes: {
				preset: [
					{
						name: 'skeleton',
						enhancements: true,
					},
					{
						name: 'wintry',
						enhancements: true,
					},
					{
						name: 'sahara',
						enhancements: true,
					},
					{
						name: 'gold-nouveau',
						enhancements: true,
					},
                    {
						name: 'rocket',
						enhancements: true,
					},
                    {
						name: 'crimson',
						enhancements: true,
					},
                    {
						name: 'hamlindigo',
						enhancements: true,
					},
                    {
						name: 'vintage',
						enhancements: true,
					},
                    {
						name: 'seafoam',
						enhancements: true,
					},
                    


				],
			},
		}),
	],
} satisfies Config;
