import fs from 'fs';

export const writeToLocalStorage = (data: Object, fileName: string) => {
	fs.writeFile(fileName, JSON.stringify(data), err => {
		if (err) return console.log(err);
		console.log('Data written to file system');
	});
};