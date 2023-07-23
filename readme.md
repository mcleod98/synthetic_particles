# Synthetic Particle Generator

This is a python program for generating simulated images of spherical or elliptical particles. Particle information is generated randomly from given statistical parameters, and this information is stored in a SQLite database. The resulting labeled dataset can be used to train models to perform general edge detection tasks.

## Getting Started

1. Pull this repository
2. Activate the virtual environment by running  `$ pipenv shell` from the project directory
3. Create settings file at `/config/mysettings.yaml` or use default file `/config/default.yaml`
4. Interact through `cli.py` entrypoint
	1.  Initialize sqlite database file and create tables `python cli.py dbinit`
	2. Generate 5 samples with the given settings: `python cli.py simulate ./config/mysettings.yaml 5`

## Configuration

The parameters used for generating each image are randomly sampled based on statistics provided in the `settings.yaml` file.

```
	name: Name of this parameter set for notekeeping purposes
	xdim: X dimension of the images to be produced
	ydim: Y dimension of the image to be produced
	mean_r: Average particle radius
	sd_r: Standard deviation of particle radius
	mean_aspect: Average particle aspect ratio
	sd_aspect: Standard deviation of aspect ratio
	mean_n: Average number of particles plotted in each image
	sd_n: Standard deviation of number of particles
	mean_theta: Average angle (in radians) of an occlusion
	sd_theta: Standard deviation of occlusions
	n_dist: A list of tuples (n, p) where n is the number of occlusions and p is the probability
	gutters: A list (gutterx, guttery) that provides the padding on the edge of the image, where particles won't be placed
    min_dist: Factor determining the minimum distance between particle centers. 0 to allow overlapping particles, 1 is approximately 1 radius of padding so particles will not quite overlap

```