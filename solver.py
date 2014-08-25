import scipy.misc
from os import listdir

def extract_digits(image):
    flooded = set()
    digits = []
    for y in xrange(len(image[0])):
        for x in xrange(len(image)):
            if tuple(image[x][y]) == (180, 150, 100) and (x, y) not in flooded:
                flooded.add((x, y))
                region = [(x, y)]
                pos = 0
                while pos < len(region):
                    xx, yy = region[pos]
                    pos += 1
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == dy == 0:
                                continue
                            if (0 <= xx + dx < len(image) and
                                0 <= yy + dy < len(image[0]) and
                                tuple(image[xx + dx][yy + dy]) == (180, 150, 100) and
                                (xx + dx, yy + dy) not in flooded):
                                region.append((xx + dx, yy + dy))
                                flooded.add((xx + dx, yy + dy))
                digits.append(region)

    if len(digits) == 5:
        return digits
    else:
        return []

N = 25
def normalized_image(pixels):
    min_x = min(x for x, y in pixels)
    min_y = min(y for x, y in pixels)
    img = [[0 for y in xrange(N)] for x in xrange(N)]
    for x, y in pixels:
        img[x - min_x][y - min_y] = 1
    return img

# Load the labeled captchas and separate them into digits
labeled_digits = []
digit_areas = [[] for i in xrange(10)]
for filename in listdir('labeled_images'):
    label = filename.split('.')[0]
    digits = extract_digits(scipy.misc.imread('labeled_images/' + filename))
    if not digits:
        print 'skipped labeled image', label
        continue
    for i, digit in enumerate(digits):
        img = normalized_image(digit)
        labeled_digits.append((int(label[i]), img))
        digit_areas[int(label[i])].append(sum(val for row in img for val in row))
        #scipy.misc.imsave('digit_{:s}_{:s}_{:d}.png'.format(label[i], label, i), img)
average_digit_area = [sum(l) / len(l) for l in digit_areas]

def solve_for_image(image):
    digits = extract_digits(image)
    if not digits:
        return
    guess = ''
    for digit in digits:
        img = normalized_image(digit)
        best = (N ** 2, None)
        for num, labeled_digit in labeled_digits:
            dist = sum(img[x][y] != labeled_digit[x][y] for x in xrange(N) for y in xrange(N))
            if abs(average_digit_area[num] - len(digit)) < 20:
                best = min(best, (dist, num))

        guess += str(best[1])

    return guess

def solve_for_filename(filename):
    return solve_for_image(scipy.misc.imread(filename))

if __name__ == '__main__':
    for i in xrange(100):
        print i, solve_for_filename('test_images/{:02d}.png'.format(i))
