const { assertFails, assertSucceeds } = require("@firebase/rules-unit-testing");
const { setup, teardown } = require("./helpers");

const mockUser = {
	uid: "alice",
};

const mockData = {
	"users/alice": {
		fullName: "Alice In Wonderland",
	},
	"users/barbaras": {
		fullName: "Barbaras In Zombieland",
	},
	"allUsers/alice": {
		fullName: "Alice In Wonderland",
	},
	"allUsers/barbaras": {
		fullName: "Barbaras In Zombieland",
	},
	"transactions/1": {
		amount: 100,
		senderId: "alice",
		recipientId: "barbaras",
	},
	"transactions/2": {
		amount: 100,
		senderId: "barbaras",
		recipientId: "alice",
	},
	"transactions/3": {
		amount: 100,
		senderId: "barbaras",
		recipientId: "catherine",
	},
	"transactions/4": {
		amount: 100,
		senderId: "alice",
		recipientId: "alice",
	},
};

describe("Database rules", () => {
	let db;

	// Applies only to tests in this describe block
	beforeAll(async () => {
		db = await setup(mockUser, mockData);
	});

	afterAll(async () => {
		await teardown();
	});

	test("allow user to read their own document in users collection", async () => {
		const ref = db.doc("users/alice");

		expect(await assertSucceeds(ref.get()));
	});

	test("deny user to read other's document in users collection", async () => {
		const ref = db.doc("users/barbaras");

		expect(await assertFails(ref.get()));
	});

	test("allow user to read their own document in allUsers collection", async () => {
		const ref = db.doc("allUsers/alice");

		expect(await assertSucceeds(ref.get()));
	});

	test("allow user to read other's document in allUsers collection", async () => {
		const ref = db.doc("allUsers/barbaras");

		expect(await assertSucceeds(ref.get()));
	});

	test("allow user to see their outgoing transaction", async () => {
		const ref = db.doc("transactions/1");

		expect(await assertSucceeds(ref.get()));
	});

	test("allow user to see their incoming transaction", async () => {
		const ref = db.doc("transactions/2");

		expect(await assertSucceeds(ref.get()));
	});

	test("allow user to see their self transaction", async () => {
		const ref = db.doc("transactions/4");

		expect(await assertSucceeds(ref.get()));
	});

	test("deny user to see other's transaction", async () => {
		const ref = db.doc("transactions/3");

		expect(await assertFails(ref.get()));
	});
});
