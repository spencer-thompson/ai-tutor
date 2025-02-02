export function decodeUnicode(str: string): string {
		return str
			.replace(/\\u[\dA-F]{4}/gi, (match) =>
				String.fromCodePoint(parseInt(match.replace(/\\u/g, ''), 16))
			)
			.replace(/\\ud[\dA-F]{3}/gi, (match) => {
				const [high, low] = match
					.split('\\u')
					.filter(Boolean)
					.map((code) => parseInt(code, 16));
				return String.fromCodePoint(((high & 0x3ff) << 10) + (low & 0x3ff) + 0x10000);
			});
	}

