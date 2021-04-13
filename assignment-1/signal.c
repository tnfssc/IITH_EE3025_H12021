#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <strings.h>
#define M_PI 3.14159265358979323846

void _fft(double complex *x, long int N, int flag)
{
  if (N <= 1)
    return;

  double complex *odd = malloc(N / 2 * sizeof(double complex));
  double complex *even = malloc(N / 2 * sizeof(double complex));
  for (long int i = 0; i < N / 2; i++)
  {
    odd[i] = x[2 * i + 1];
    even[i] = x[2 * i];
  }

  _fft(even, N / 2, flag);
  _fft(odd, N / 2, flag);

  for (int i = 0; i < N / 2; i++)
  {
    double complex w = cexp(2 * M_PI * i * -I * flag / N);
    x[i] = even[i] + w * odd[i];
    x[i + N / 2] = even[i] - w * odd[i];
  }

  free(odd);
  free(even);

  return;
}

void fft(double complex *x, long int N)
{
  _fft(x, N, 1);
  return;
}

void ifft(double complex *x, long int N)
{

  _fft(x, N, -1);

  for (int i = 0; i < N; i++)
    x[i] = x[i] / N;

  return;
}

void main()
{
  int n = (1 << 20);

  double complex *X1 = (double complex *)malloc(n * sizeof(double complex));
  double complex *X2 = (double complex *)malloc(n * sizeof(double complex));

  FILE *ft1, *ft2, *fF1, *ff1, *fF2, *ff2;

  ft1 = fopen("Sound_Noise.dat", "r");
  ft2 = fopen("Sound_Low_Noise.dat", "r");

  int len = 0;
  char temp[30];
  char *ptr;
  while (fscanf(ft1, "%30[^\n]\n", temp) != EOF && len < n)
  {
    X1[len] = CMPLX(strtod(temp, &ptr), 0);
    len++;
  }
  len = 0;
  while (fscanf(ft2, "%30[^\n]\n", temp) != EOF && len < n)
  {
    X2[len] = CMPLX(strtod(temp, &ptr), 0);
    len++;
  }

  fft(X1, n);
  fF1 = fopen("Sound_Noise_FFT.dat", "w");
  for (int i = 0; i < n; i++)
    fprintf(fF1, "%1f+%1fi\n", creal(X1[i]), cimag(X1[i]));

  ifft(X1, n);
  ff1 = fopen("Sound_Noise_IFFT.dat", "w");
  for (int i = 0; i < n; i++)
    fprintf(ff1, "%1f\n", creal(X1[i]));

  fft(X2, n);
  fF2 = fopen("Sound_Low_Noise_FFT.dat", "w");
  for (int i = 0; i < n; i++)
    fprintf(fF2, "%1f+%1fi\n", creal(X2[i]), cimag(X2[i]));

  ifft(X2, n);
  ff2 = fopen("Sound_Low_Noise_IFFT.dat", "w");
  for (int i = 0; i < n; i++)
    fprintf(ff2, "%1f\n", creal(X2[i]));

  fclose(ft1);
  fclose(ft2);
  fclose(fF1);
  fclose(fF2);
  fclose(ff1);
  fclose(ff2);
}
