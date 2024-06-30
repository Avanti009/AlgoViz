import pygame
import random
import math
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('Times Roman ', 15)
	LARGE_FONT = pygame.font.SysFont('Times Roman', 30)

	SIDE_PAD = 200
	TOP_PAD = 300

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending, algorithm_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start | A- Ascending | D- Descending | I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render(algorithm_info, 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
	

    draw_list(draw_info)
    pygame.display.update()

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
    algorithm_info = "Bubble Sort: Repeatedly swaps adjacent elements until the list is sorted."
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    algorithm_info = "Insertion Sort: Builds the final sorted array by iteratively inserting elements into their correct positions.."
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst
def merge_sort(draw_info, ascending=True):
    algorithm_info = "Merge Sort:Stable and efficient algorithm dividing, sorting, and merging sub-lists until a fully sorted list is obtained."

    def merge(lst, left, mid, right):
        left_copy = lst[left:mid + 1]
        right_copy = lst[mid + 1:right + 1]

        left_idx = right_idx = 0
        sorted_idx = left

        while left_idx < len(left_copy) and right_idx < len(right_copy):
            if (left_copy[left_idx] <= right_copy[right_idx] and ascending) or \
               (left_copy[left_idx] >= right_copy[right_idx] and not ascending):
                lst[sorted_idx] = left_copy[left_idx]
                left_idx += 1
            else:
                lst[sorted_idx] = right_copy[right_idx]
                right_idx += 1

            draw_list(draw_info, {left + left_idx: draw_info.GREEN, mid + 1 + right_idx: draw_info.RED}, True)
            yield True
            sorted_idx += 1

        while left_idx < len(left_copy):
            lst[sorted_idx] = left_copy[left_idx]
            draw_list(draw_info, {left + left_idx: draw_info.GREEN}, True)
            yield True
            left_idx += 1
            sorted_idx += 1

        while right_idx < len(right_copy):
            lst[sorted_idx] = right_copy[right_idx]
            draw_list(draw_info, {mid + 1 + right_idx: draw_info.RED}, True)
            yield True
            right_idx += 1
            sorted_idx += 1

    def merge_sort_helper(lst, left, right):
        if left < right:
            mid = (left + right) // 2
            yield from merge_sort_helper(lst, left, mid)
            yield from merge_sort_helper(lst, mid + 1, right)
            yield from merge(lst, left, mid, right)

    lst = draw_info.lst
    yield from merge_sort_helper(lst, 0, len(lst) - 1)
    return lst

def quick_sort(draw_info, ascending=True):
    algorithm_info = "Quick Sort:Efficient divide-and-conquer sorting using pivot elements for recursive partitioning.."

    def partition(lst, low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True

        return i + 1

    def quick_sort_helper(lst, low, high):
        if low < high:
            pi = yield from partition(lst, low, high)
            yield from quick_sort_helper(lst, low, pi - 1)
            yield from quick_sort_helper(lst, pi + 1, high)

    lst = draw_info.lst
    yield from quick_sort_helper(lst, 0, len(lst) - 1)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    algorithm_info = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            if algorithm_info:
                draw(draw_info, sorting_algo_name, ascending, algorithm_info)
            else:
                draw(draw_info, sorting_algo_name, ascending , algorithm_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                algorithm_info = None  # Clear algorithm info when starting a new sorting process
            elif event.key == pygame.K_a and not sorting:
                ascending = True
                algorithm_info = None
            elif event.key == pygame.K_d and not sorting:
                ascending = False
                algorithm_info = None
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
                algorithm_info = "Insertion Sort: Builds the final sorted array by iteratively inserting elements into their correct positions."
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
                algorithm_info = "Bubble Sort: Repeatedly swaps adjacent elements until the list is sorted."
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
                algorithm_info = "Merge Sort:Stable and efficient algorithm dividing, sorting, and merging sub-lists until a fully sorted list is obtained.."
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
                algorithm_info = "Quick Sort:Builds the final sorted array by iteratively inserting elements into their correct positions."

    pygame.quit()

if __name__ == "__main__":
    main()





































































































            