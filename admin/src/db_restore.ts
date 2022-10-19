import fs from 'fs';
import {db} from './init_firebase';
import {writeToLocalStorage} from './utils';

export const saveFirestoreState = async () => {
	interface DbInterface {
		[id: string]: {
			[id: string]: Object;
		};
	}
	const database: DbInterface = {};

	const ref = await db.listCollections();

	for await (const col of ref) {
		const docs = await col.get();

		const collectionName = col.path;
		database[collectionName] = {};

		docs.forEach(d => {
			database[collectionName][d.id] = d.data();
		});
	}

	const now = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
	const fileName = `${now}_DBState.json`;
	writeToLocalStorage(database, fileName);
};

export const deleteFirestore = async () => {
	interface DbInterface {
		[id: string]: Array<string>;
	}
	const database: DbInterface = {};

	const ref = await db.listCollections();

	for await (const col of ref) {
		const docs = await col.get();

		const collectionName = col.path;
		database[collectionName] = [];

		docs.forEach(d => {
			database[collectionName].push(d.id);
		});
	}

	Object.keys(database).map(async colName => {
		const ref = db.collection(colName);

		for await (const id of database[colName]) {
			await ref.doc(id).delete();
		}
	});
};

export const restoreDbFromFile = async (filePath: string) => {
	// const filePath = path.join(
	// 	'/home/soul/Projects/card-pay/temp/',
	// 	'2022-10-08 01:00:05_DBState.json'
	// );

	fs.readFile(filePath, { encoding: 'utf-8' }, async (err, data) => {
		if (err) console.log(err);
		else {
			const dbData = JSON.parse(data);

			for await (const collectionName of Object.keys(dbData)) {
				const colRef = db.collection(collectionName);

				for await (const docId of Object.keys(dbData[collectionName])) {
					await colRef
						.doc(docId)
						.create(dbData[collectionName][docId]);
				}
			}
		}
	});
};