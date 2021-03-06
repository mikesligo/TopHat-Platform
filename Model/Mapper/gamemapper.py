import mapper
import Model.game
import usermapper as UM

class GameMapper(mapper.Mapper):

	def __init__(self):
		super(GameMapper, self).__init__()

	def targetClass(self):
		return "Game"

	def tableName(self):
		return "games"

	def _selectStmt(self):
		return "SELECT g.*, t.name as game_type_name FROM games g LEFT JOIN game_types t ON g.game_type_id = t.id WHERE g.id = %s LIMIT 1"

	def _selectAllStmt(self):
		return "SELECT g.*, t.name as game_type_name FROM games g LEFT JOIN game_types t ON g.game_type_id = t.id LIMIT %s, %s"	

	def _deleteStmt(self, obj):
		return "DELETE FROM games WHERE id = %s LIMIT 1"
		
	def _doCreateObject(self, data):
		"""Builds the game object given the draw data returned from the database query"""
		game_ = Model.game.Game(data["id"])

		# get creator User object
		UserMapper = UM.UserMapper()
		creator = UserMapper.find(data["creator"])
		game_.setCreator(creator)

		game_.setName(data["name"])
		game_.setGameTypeId(data["game_type_id"])
		game_.setGameTypeName(data["game_type_name"])
		game_.setTime(data["time"])

		return game_

	def _doInsert(self, obj):
		# build query
		# id, name, game_type_id, creator
		query = "INSERT INTO games VALUES(NULL, %s, %s, %s, NULL)"

		# convert boolean value to int bool
		params = (obj.getName(), obj.getGameTypeId(), obj.getCreator().getId())

		# run the query
		cursor = self.db.getCursor()
		rowsAffected = cursor.execute(query, params)

		# get insert id
		id_ = cursor.lastrowid
		obj.setId(id_)

		cursor.close()

		# only if rows were changed return a success response
		if rowsAffected > 0:
			return True
		else:
			return False

	def _doUpdate(self, obj):
		# build the query
		query = "UPDATE games SET name = %s, game_type_id = %s, creator = %s WHERE id = %s LIMIT 1"
		params = (obj.getName(), obj.getGameTypeId(), obj.getCreator().getId(), obj.getId())

		# run the query
		cursor = self.db.getCursor()
		rowsAffected = cursor.execute(query, params)
		cursor.close()

		if rowsAffected > 0:
			return True
		else:
			return False