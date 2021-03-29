let slide_index = 1;
let time = 0;
let timing = true;
const slidenum_display = document.getElementById("slidenum");
const timer = document.getElementById("timer");
const speed = document.getElementById("speed");

show_slides(slide_index, slide_index);

plus_slides = (n) => show_slides(slide_index, slide_index += n);

current_slide = (n) => show_slides(slide_index, slide_index = n);

function toggle_timing()
{
	timing = !timing;
	time = 0;
	if (timing) {
		timer.innerHTML = "";
		return;
	}

	speed.value = 0;
	speed.oninput();

	timer.style.width = "100%";
	timer.style.opacity = "100%";
	timer.innerHTML = "PAUSED";
}

function show_slides(a, n)
{
	let slides = document.getElementsByClassName("slides");
	let dots = document.getElementsByClassName("dot");

	if (n > slides.length)
		n = slide_index = 1;
	else if (n < 1)
		n = slide_index = slides.length;

	let was_timing = timing;
	timing = false;

	document.querySelectorAll("button")
		.forEach((_el) => _el.disabled = true);
	
	fade = (x, s) => () => {
		if (x)
		{
			window.setTimeout(fade(x-1, s), s);
			slides[a-1].style.opacity = x + '%';
			if (was_timing)
				timer.style.opacity =
					(time - time*time/100)*x/30 + '%';
			return;
		}
		slides[a-1].style.display = "none";
		slides[a-1].style.opacity = null;
		dots[a-1].className=dots[a-1].className.replace(" active", "");
		slides[n-1].style.display = "block";
		dots[n-1].className += " active";
		slidenum_display.innerHTML = n;
		time = 0;
		timing = was_timing;
		document.querySelectorAll("button")
			.forEach((_el) => _el.disabled = false);
		return;
	};

	fade(100, Math.ceil(Math.exp(-speed.value / 100) * 3))();
}

speed.oninput = () => {
	let ts = document.getElementById("timer_span").style;
	ts.margin = "0 " + (40.5 + speed.value / 40) + '%';
	ts.width  = 18 - speed.value / 20 + '%';
}

window.setInterval(() => {
	if (!timing)
		return;
	
	time += Math.exp(speed.value / 100) / 10;

	if (time >= 100)
	{
		time = 0;
		plus_slides(1);
	}

	timer.style.width = time + '%';
	timer.style.opacity = (100*time - time*time)/30 + '%';
}, 3);