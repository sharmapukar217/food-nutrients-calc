export const load = async ({ fetch }) => {
	const ageGroupsResponse = await fetch('http://localhost:5000/age-groups');
	const ageGroups = await ageGroupsResponse.json();

	const foodsResponse = await fetch('http://localhost:5000/foods');
	const foods = await foodsResponse.json();

	return { ageGroups, foods };
};
