<script lang="ts">
	import AutoComplete from 'simple-svelte-autocomplete';

	let result = null
	async function searchColor(keyword) {
		return ['White', 'Red', 'Yellow', 'Green', 'Blue', 'Black', 'Mät bläck', '<i>Jét Black</i>'];
	}

	let ageGroup = null
	let breakfastItems = [];
	let breakfastGrams = '';

	let lunchItems = [];
	let lunchGrams = '';

	let snacksItems = [];
	let snacksGrams = '';

	let supperItems = [];
	let supperGrams = '';

	const handleSubmit = async (ev) => {
		result = null
		ev.preventDefault();

		const formData = {
			ageGroup,
			breakfast: breakfastItems.map((item, index) => `${item} ${breakfastGrams.split(',')[index]}`).join(', '),
			lunch: lunchItems.map((item, index) => `${item} ${lunchGrams.split(',')[index]}`).join(', '),
			snacks: snacksItems.map((item, index) => `${item} ${snacksGrams.split(',')[index]}`).join(', '),
			supper: supperItems.map((item, index) => `${item} ${supperGrams.split(',')[index]}`).join(', '),
		}


		const response = await fetch("http://localhost:5000/nutrient-intake", {
			method: "POST",
			body: JSON.stringify(formData),
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json",
			}
		});

		const json = await response.json()
		result = json
	};
	export let data;
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

{#if result}
	<pre>{JSON.stringify(result, null, 2)}</pre>
	{/if}
<form on:submit={handleSubmit}>
	<select bind:value={ageGroup}>
		{#each data.ageGroups as age}
			<option value={age}> {age} </option>
		{/each}
	</select>

	<br />

	<AutoComplete
		multiple
		items={data.foods}
		bind:selectedItem={breakfastItems}
		placeholder="Enter food items consumed for breakfast"
	/>

	<input
		required
		type="text"
		name="grams"
		placeholder="Enter number in grams, comma separated"
		bind:value={breakfastGrams}
	/>

	<br />

	<AutoComplete
		multiple
		items={data.foods}
		bind:selectedItem={lunchItems}
		placeholder="Enter food items consumed for lunch"
	/>

	<input
		required
		type="text"
		name="grams"
		placeholder="Enter number in grams, comma separated"
		bind:value={lunchGrams}
	/>

	<br />

	<AutoComplete
		multiple
		items={data.foods}
		bind:selectedItem={snacksItems}
		placeholder="Enter food items consumed for snacks"
	/>

	<input
		required
		type="text"
		name="grams"
		placeholder="Enter number in grams, comma separated"
		bind:value={snacksGrams}
	/>

	<br />

	<AutoComplete
		multiple
		items={data.foods}
		bind:selectedItem={supperItems}
		placeholder="Enter food items consumed for supper"
	/>

	<input
		required
		type="text"
		name="grams"
		placeholder="Enter number in grams, comma separated"
		bind:value={supperGrams}
	/>

	<br />
	<button type="submit">Submit</button>
</form>
