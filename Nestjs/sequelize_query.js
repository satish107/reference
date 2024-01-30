User.findAll({
	attributes: ['name', 'email']
})

User.findAll({
	attributes: ['name', 'email', sequelize.fn('COUNT', Sequelize.col('coin')),'n_coin']
})

User.findAll({
	attributes: {
		include: ['name', 'email']
	}
})

User.findAll({
	attributes: {
		exclude: ['name', 'email']
	}
})

// WHERE clauses

Post.findAll({
	where: {
		postId: 1,
		postName: 'post title',
		status: 'Active'
	}
})

Post.destroy({
	where: {
		authorId: {
			[Op.OR]: [12, 13]
		}
	}
})

// UPDATE queries

User.update({lastname: 'Joe'}, {
	where: {
		lastname: null
	}
})

User.destroy({
	where: {
		lastname: 'Joe'
	}
})

User.destroy({
	truncate: true
})

// Ordering

SubTask.findAll({
	order: ['title', 'DESC'],
	sequelize.fn('max', sequelize.col('title')),
	[sequelize.fn('max', sequelize.col('title')), 'DESC'],
	[sequelize.fn('other_function', sequelize.col('col1'), 0, 'lalala'), 'DESC'],
	[Task, 'createAt', 'DESC'],
	[Task, Project, 'createAt', 'DESC'],
})
order: sequelize.literal('max(age) DESC')
order: sequelize.fn('max', sequelize.col('age'))











