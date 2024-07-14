extends Node3D

const SPEED = 40.0

@onready var mesh = $MeshInstance3D
@onready var ray = $RayCast3D
@onready var particles = $GPUParticles3D
# Called when the node enters the scene tree for the first time.
func _ready():
	var random_angle_y = randf_range(-5,5)
	var random_angle_x = randf_range(-5,5)
	var random_angle_rad_y = deg_to_rad(random_angle_y)
	var random_angle_rad_x = deg_to_rad(random_angle_x)
	
	rotate(basis.x, random_angle_rad_x)
	rotate(basis.y, random_angle_rad_y)
	
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):

	global_position += global_transform.basis * Vector3(0,0, -SPEED) * delta
	if ray.is_colliding():
		mesh.visible = false
		particles.emitting = true
		ray.enabled = false
		if ray.get_collider().is_in_group("enemy"):
			ray.get_collider().hit()
		await get_tree().create_timer(1.0).timeout
		queue_free()
		


func _on_timer_timeout():
	queue_free()
	
