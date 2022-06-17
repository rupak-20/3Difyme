import albumentations as A
import albumentations.pytorch as AT
import cv2


class ImgTransformer:
    def __init__(self, img_size, color_aug=False):
        self.img_size = img_size
        self.color_aug = color_aug

    def transform(self, image, mask):
        if self.color_aug:
            transforms = A.Compose(
                [
                    A.Resize(self.img_size, self.img_size),
                    A.OneOf(
                        [
                            A.IAAAdditiveGaussianNoise(),
                            A.GaussNoise(var_limit=(100, 200)),
                            A.JpegCompression(quality_lower=75, p=0.2),
                        ],
                        p=0.3,
                    ),
                    A.OneOf(
                        [
                            A.MotionBlur(blur_limit=10, p=0.2),
                            A.MedianBlur(blur_limit=11, p=0.1),
                            A.Blur(blur_limit=11, p=0.1),
                        ],
                        p=0.3,
                    ),
                    A.ShiftScaleRotate(shift_limit=0, scale_limit=(-0.1, 0.4), rotate_limit=5, p=0.6),
                    A.Cutout(num_holes=8, max_h_size=48, max_w_size=48, p=0.3),
                    A.OneOf(
                        [
                            A.CLAHE(clip_limit=4),
                            A.IAASharpen(),
                            A.IAAEmboss(),
                            A.RandomBrightnessContrast(),
                        ],
                        p=0.5,
                    ),
                    A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=50, val_shift_limit=50, p=0.5),
                ]
            )
        else:
            transforms = A.Compose(
                [
                    A.Resize(self.img_size, self.img_size),
                ]
            )

        image_norm_and_to_tensor = A.Compose(
            [
                A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
                AT.ToTensorV2(transpose_mask=True),
            ]
        )
        mask_norm_and_to_tensor = A.Compose(
            [
                A.Normalize(mean=[0.0, 0.0, 0.0], std=[1, 1, 1]),
                AT.ToTensorV2(transpose_mask=True),
            ]
        )

        transform_pair = transforms(image=image, mask=mask)
        transform_image = transform_pair["image"]
        transform_mask = transform_pair["mask"]

        transform_image = image_norm_and_to_tensor(image=transform_image)["image"]
        transform_mask = mask_norm_and_to_tensor(image=transform_mask)["image"]

        return transform_image, transform_mask

    def load(self, impath, maskpath):
        image = cv2.imread(impath, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mask = cv2.imread(maskpath)
        return self.transform(image, mask)
