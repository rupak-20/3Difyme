import numpy as np


def create_figure(img, mask, prediction, dye=False):
    return create_multi_figure([[img, mask, prediction]], dye)


def create_multi_figure(rows):
    img = rows[0].cpu()
    mask = rows[-1].cpu()

    # reverse normalization of the orignal image
    img = (img + 1) / 2
    rows[0] = img

    for j, d in enumerate(rows):
        d = d.squeeze()
        im = d.data.cpu().numpy()

        if im.shape[0] != 3:
            im = np.expand_dims(im, axis=0)
            im = np.concatenate((im, im, im), axis=0)

        im = im.transpose(1, 2, 0)

        if j == 0:
            img = im
        else:
            mask = im
    
    img = img*255
    # img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    # cv.imwrite('hair_mask.jpg', mask)
    # cv.imwrite('original_img.jpg', img)
    img = img*mask
    # cv.imwrite('hair_segment.jpg', img)
    total = 0
    hair_color_rgb = np.zeros((1,3))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j][0]!=0 and img[i][j][1]!=0 and img[i][j][2]!=0:
                total += 1
                hair_color_rgb = hair_color_rgb + img[i][j]
    
    hair_color_rgb = hair_color_rgb/total
    hair_color_rgb = hair_color_rgb.astype('int')
    
    return hair_color_rgb
    
