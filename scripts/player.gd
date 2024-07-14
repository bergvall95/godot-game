extends CharacterBody3D

# movement vals
var speed 
const WALK_SPEED = 5.0
const SPRINT_SPEED = 8.0
const JUMP_VELOCITY = 4.5
const SENSITIVITY = 0.003
const AIR_CONTROL_MOD = 1.0
const HIT_STAGGER = 8.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = 9.8
var direction = 0.0

# player experience vals
const BOB_FREQ = 2.0
const BOB_AMP= 0.03
var t_bob= 0.0

# fov variables
const BASE_FOV = 75.0
const FOV_CHANGE = 1.5

# player health 
var health = 10.0
# signal
signal player_hit

# Bullets
var bullet = load("res://Scenes/weapons/bullet.tscn")
func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

@onready var head = $head
@onready var camera = $head/playercam
@onready var gun_anim = $head/playercam/uziSilencer2/AnimationPlayer
@onready var gun_barrel = $head/playercam/uziSilencer2/RayCast3D
@onready var gun_anim2 = $head/playercam/uziSilencer3/AnimationPlayer
@onready var gun_barrel2 = $head/playercam/uziSilencer3/RayCast3D

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		head.rotate_y(-event.relative.x * SENSITIVITY)
		camera.rotate_x(-event.relative.y * SENSITIVITY)
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(-90), deg_to_rad(90));

func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Handle jump.
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	var input_dir = Input.get_vector("left", "right", "up", "down")
	

	direction = (head.transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	# handle sprint
	if Input.is_action_pressed('sprint'):
		speed = SPRINT_SPEED
	else: 
		speed = WALK_SPEED
		
	if is_on_floor():
		if direction:
			velocity.x = direction.x * speed
			velocity.z = direction.z * speed
		else:
			velocity.x = lerp(velocity.x, direction.x * speed, delta * 7.0)
			velocity.z = lerp(velocity.z, direction.z * speed, delta * 7.0)
	else: 
		velocity.x = lerp(velocity.x, direction.x * speed, delta * 2.0)
		velocity.z = lerp(velocity.z, direction.z * speed, delta * 2.0)
	# head bob
	t_bob += delta * velocity.length() * float(is_on_floor())
	camera.transform.origin = _headbob(t_bob)
	
	# FOV 
	var velocity_clamped = clamp(velocity.length(), 0.5, SPRINT_SPEED * 2)
	var target_fov = BASE_FOV + FOV_CHANGE * velocity_clamped
	camera.fov = lerp(camera.fov, target_fov, delta * 8.0)
	
	if Input.is_action_pressed("shoot"):
		if !gun_anim.is_playing():
			gun_anim.play("shoot")
			gun_anim2.play("shoot")
			_instantiate_bullet( gun_barrel)
			_instantiate_bullet( gun_barrel2)
			
			
	
	move_and_slide()
	

func _instantiate_bullet( barrel):
	var instance = bullet.instantiate()
	instance.position = barrel.global_position
	instance.transform.basis = barrel.global_transform.basis
	get_parent().add_child(instance)
	
func _headbob(time) -> Vector3:
	var pos = Vector3.ZERO
	pos.y = sin(time * BOB_FREQ ) * BOB_AMP
	pos.x = cos(time * BOB_FREQ) * BOB_AMP
	return pos
		
func hit(dir):
	emit_signal("player_hit")
	velocity += dir * HIT_STAGGER
	health -=2
	if (health < 0):
		queue_free()
	
		
