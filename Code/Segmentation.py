# Pixel-wise Vector Quantization (VQ) of an image # Color clustering# Color quantizationimport numpy as npimport matplotlib.pyplot as pltfrom matplotlib import colorsfrom sklearn.cluster import KMeans, DBSCANfrom sklearn.mixture import GaussianMixturefrom sklearn.utils import shufflefrom time import timeimport cv2import scipy.statsimport skfuzzy as fuzz# ------------------------------------------------------------# Define a function to display the result of clustering alogrithmsdef recreate_image(codebook, labels, w, h):    d = codebook.shape[1]    image = np.zeros((w, h, d))    label_idx = 0    for i in range(w):        for j in range(h):            image[i][j] = codebook[labels[label_idx]]            label_idx += 1    return image# ------------------------------------------------------------# Specify the number of colors n_colors = 64# Load the photo and convert from BGR to RGB modelimg_bgr = cv2.imread("./Images/face.jpg")img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)# Convert to gray scaleimg_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)# Converts to float instead of integer and divided by 255img = np.array(img, dtype = np.float64) / 255# Transform to a 2D numpy arrayw, h, d = original_shape = tuple(img.shape)image_array = np.reshape(img, (w*h, d))# Display two results, alongside original imagefig, ax = plt.subplots(1, 2, figsize = (16, 8), subplot_kw = dict(xticks=[], yticks=[]))fig.subplots_adjust(wspace=0.05)ax[0].imshow(img)ax[0].set_title('Original Image', size=16)ax[1].imshow(img_gray, cmap='gray')ax[1].set_title('Gray Scale Image', size=16)# Fitting K-means using the whole image data t0 = time()image_array_sample = shuffle(image_array, random_state = 0)kmeans = KMeans(n_clusters = n_colors, random_state = 0).fit(image_array_sample)print("K-means is done in %0.3fs." % (time() - t0))# Get k-means labels for all pointskmeans_labels = kmeans.predict(image_array)# Fitting Gaussian Mixed Model using the whole image datat0 = time()image_array_sample = shuffle(image_array, random_state = 0)gmm = GaussianMixture(n_components = n_colors, init_params = 'random', random_state = 0, covariance_type = "full").fit(image_array_sample)print("done in %0.3fs." % (time() - t0))# Get gmm labels for all pointsgmm_labels = gmm.predict(image_array)# Create centroid of each clusters in GMM's predictiongmm_centers = np.empty(shape = (gmm.n_components, d), dtype = np.float64)for i in range(gmm.n_components):    density = scipy.stats.multivariate_normal(cov=gmm.covariances_[i], mean=gmm.means_[i]).logpdf(image_array)    gmm_centers[i, :] = image_array[np.argmax(density)]# Display two results, alongside original imagefig, ax = plt.subplots(1, 2, figsize = (16, 8), subplot_kw = dict(xticks=[], yticks=[]))fig.subplots_adjust(wspace=0.05)ax[0].imshow(img)ax[0].set_title('Original Image', size=16)ax[1].imshow(recreate_image(kmeans.cluster_centers_, kmeans_labels, w, h))ax[1].set_title('{}-color Image with K-means'.format(n_colors), size=16)### DBSCANimage_seg = recreate_image(kmeans.cluster_centers_, kmeans_labels, w, h)image_1d_seg = image_seg.reshape((-1, 1))dbscan = DBSCAN(eps = 0.8, min_samples = 100)y_dbscan = dbscan.fit_predict(image_1d_seg)