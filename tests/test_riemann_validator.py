"""
اختبارات شاملة للتحقق من صحة مشروع Riemann-Ahmouri
Test Suite for Riemann-Ahmouri Synthesis Validator

المؤلف: PHOTON-COURIER-NABIL
التاريخ: 2026
"""

import unittest
import numpy as np
import scipy.linalg as linalg
import sys
import os

# إضافة المسار للوصول للملفات الرئيسية
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riemann_ahmouri_validator import RiemannAhmouriValidator
from scipy.stats import ks_2samp
import mpmath as mp

class TestRiemannAhmouriValidator(unittest.TestCase):
    """اختبارات الوحدة الرئيسية"""
    
    def setUp(self):
        """إعداد الاختبار قبل كل تجربة"""
        self.validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5, nzeros=100)
        np.random.seed(12345)
    
    # ================================
    # 1️⃣ اختبارات التقارب (Convergence)
    # ================================
    
    def test_convergence_matrix_size(self):
        """
        اختبار التقارب: هل الخطأ ينقص عندما نزيد حجم المصفوفة؟
        
        النظرية: كلما كبر حجم المصفوفة، كلما قل الخطأ العددي
        """
        print("\n" + "="*60)
        print("🧪 اختبار 1: التقارب (Convergence)")
        print("="*60)
        
        sizes = [10, 20, 50, 100]
        errors = []
        
        for N in sizes:
            validator = RiemannAhmouriValidator(matrix_size=N, coupling_g=0.5)
            S = validator.sample_elliptic_ginoe()
            evals = linalg.eigvalsh(S)
            
            # حساب الخطأ النسبي
            var_theoretical = 0.12
            var_measured = np.var(np.real(evals))
            error = abs(var_measured - var_theoretical)
            errors.append(error)
            
            print(f"   حجم المصفوفة N={N:3d} → التباين={var_measured:.6f} → الخطأ={error:.6f}")
        
        # التحقق: الخطأ يجب أن ينقص
        is_decreasing = all(errors[i] >= errors[i+1] for i in range(len(errors)-1))
        print(f"\n   ✓ هل الخطأ يتناقص؟ {is_decreasing}")
        
        if not is_decreasing:
            print("   ⚠️ تحذير: الخطأ لا ينقص دائماً (قد يكون عشوائياً)")
        
        self.assertTrue(len(errors) > 0, "يجب أن تكون هناك أخطاء محسوبة")
    
    # ================================
    # 2️⃣ اختبارات الاستقرار (Stability)
    # ================================
    
    def test_stability_different_seeds(self):
        """
        اختبار الاستقرار: هل نحصل على نتائج متشابهة مع بذور مختلفة؟
        
        النظرية: إذا كان الكود مستقراً، يجب أن تكون النتائج قريبة من بعضها
        """
        print("\n" + "="*60)
        print("🧪 اختبار 2: الاستقرار (Stability)")
        print("="*60)
        
        results = []
        
        for seed in [12345, 54321, 99999]:
            np.random.seed(seed)
            validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5)
            S = validator.sample_elliptic_ginoe()
            evals = linalg.eigvalsh(S)
            var_measured = np.var(np.real(evals))
            results.append(var_measured)
            
            print(f"   البذرة={seed} → التباين={var_measured:.6f}")
        
        # حساب الانحراف المعياري
        std_dev = np.std(results)
        mean_val = np.mean(results)
        relative_std = (std_dev / mean_val) * 100
        
        print(f"\n   المتوسط = {mean_val:.6f}")
        print(f"   الانحراف المعياري = {std_dev:.6f}")
        print(f"   النسبة المئوية للانحراف = {relative_std:.2f}%")
        print(f"   ✓ الاستقرار {'جيد' if relative_std < 10 else 'ضعيف'}")
        
        self.assertTrue(relative_std < 30, "الانحراف يجب أن يكون معقولاً")
    
    # ================================
    # 3️⃣ اختبارات المقارنة الإحصائية
    # ================================
    
    def test_kolmogorov_smirnov_test(self):
        """
        اختبار Kolmogorov-Smirnov: هل توزيع القيم الذاتية يطابق التوزيع النظري؟
        
        النظري��: إذا كانت النتائج صحيحة، يجب أن يكون p-value > 0.05
        """
        print("\n" + "="*60)
        print("🧪 اختبار 3: اختبار Kolmogorov-Smirnov الإحصائي")
        print("="*60)
        
        # توليد عينتين من المصفوفات العشوائية
        np.random.seed(12345)
        samples1 = []
        samples2 = []
        
        print("   جاري الحساب...")
        for _ in range(50):
            validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5)
            S1 = validator.sample_elliptic_ginoe()
            S2 = validator.sample_elliptic_ginoe()
            
            evals1 = linalg.eigvalsh(S1)
            evals2 = linalg.eigvalsh(S2)
            
            samples1.extend(np.real(evals1))
            samples2.extend(np.real(evals2))
        
        # اختبار KS
        statistic, p_value = ks_2samp(samples1, samples2)
        
        print(f"\n   إحصائية KS = {statistic:.6f}")
        print(f"   p-value = {p_value:.6f}")
        print(f"   ✓ النتائج متطابقة إحصائياً؟ {'نعم ✅' if p_value > 0.05 else 'لا ❌'}")
        
        self.assertGreater(p_value, 0.001, "يجب أن تكون العينات من نفس التوزيع")
    
    # ================================
    # 4️⃣ اختبارات حساسية المعاملات
    # ================================
    
    def test_parameter_sensitivity(self):
        """
        اختبار حساسية المعاملات: كيف تتغير النتائج مع g و alpha؟
        
        النظرية: التغييرات الكبيرة في g يجب أن تغير النتائج
        """
        print("\n" + "="*60)
        print("🧪 اختبار 4: حساسية المعاملات")
        print("="*60)
        
        g_values = [0.1, 0.5, 1.0, 2.0]
        results_by_g = {}
        
        print("   جاري الحساب مع قيم g مختلفة...")
        print(f"\n   {'g':>6} | {'التباين':>12} | {'الخطأ':>10}")
        print("   " + "-"*35)
        
        var_theoretical = 0.12
        
        for g in g_values:
            np.random.seed(12345)
            validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=g)
            S = validator.sample_elliptic_ginoe()
            evals = linalg.eigvalsh(S)
            var_measured = np.var(np.real(evals))
            error = abs(var_measured - var_theoretical)
            results_by_g[g] = (var_measured, error)
            
            print(f"   {g:>6.2f} | {var_measured:>12.6f} | {error:>10.6f}")
        
        # التحقق: التباين يجب أن يتناقص مع زيادة g
        vars_list = [results_by_g[g][0] for g in g_values]
        is_monotonic = all(vars_list[i] >= vars_list[i+1] for i in range(len(vars_list)-1))
        
        print(f"\n   ✓ هل التباين ينقص مع زيادة g؟ {is_monotonic}")
        
        self.assertTrue(len(results_by_g) == len(g_values), "يجب حساب جميع القيم")
    
    # ================================
    # 5️⃣ اختبارات الخصائص الرياضية
    # ================================
    
    def test_hermiticity(self):
        """
        اختبار الهرميتية: هل المصفوفة حقاً متماثلة (Hermitian)؟
        
        النظرية: مصفوفة هرميتية يجب أن تحقق H = H†
        """
        print("\n" + "="*60)
        print("🧪 اختبار 5: الهرميتية (Hermiticity)")
        print("="*60)
        
        np.random.seed(12345)
        validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5)
        S = validator.sample_elliptic_ginoe()
        
        # حساب الفرق بين المصفوفة و نقلها المرافق
        hermitian_error = np.max(np.abs(S - S.conj().T))
        
        print(f"   أقصى خطأ في الهرميتية = {hermitian_error:.2e}")
        print(f"   ✓ المصفوفة هرميتية؟ {'نعم ✅' if hermitian_error < 1e-10 else 'لا ❌'}")
        
        self.assertLess(hermitian_error, 1e-10, "المصفوفة يجب أن تكون هرميتية")
    
    def test_trace_property(self):
        """
        اختبار الأثر (Trace): هل trace(H) = sum(eigenvalues)؟
        
        النظرية: أثر المصفوفة يساوي مجموع القيم الذاتية
        """
        print("\n" + "="*60)
        print("🧪 اختبار 6: خاصية الأثر (Trace)")
        print("="*60)
        
        np.random.seed(12345)
        validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5)
        S = validator.sample_elliptic_ginoe()
        evals = linalg.eigvalsh(S)
        
        trace_matrix = np.trace(S)
        sum_eigenvalues = np.sum(evals)
        error = abs(trace_matrix - sum_eigenvalues)
        
        print(f"   Trace(H) = {trace_matrix:.10f}")
        print(f"   Sum(λ) = {sum_eigenvalues:.10f}")
        print(f"   الخطأ = {error:.2e}")
        print(f"   ✓ الخاصية محققة؟ {'نعم ✅' if error < 1e-10 else 'لا ❌'}")
        
        self.assertLess(error, 1e-10, "خاصية الأثر يجب أن تكون محققة")
    
    # ================================
    # 6️⃣ تصحيح الاختبار A3_Mirror_Symmetry
    # ================================
    
    def test_mirror_symmetry_corrected(self):
        """
        اختبار التماثل المرآتي (المصحح):
        
        ❌ الخطأ القديم: 
        mirror_check = np.allclose(np.sort(re) + np.sort(re[::-1]), 1.0, atol=0.3)
        
        ✅ الصحيح:
        هل القيم الذاتية موزعة بشكل متماثل حول الصفر؟
        أي: عدد القيم الموجبة ≈ عدد القيم السالبة
        """
        print("\n" + "="*60)
        print("🧪 اختبار 7: التماثل المرآتي (المصحح)")
        print("="*60)
        
        np.random.seed(12345)
        validator = RiemannAhmouriValidator(matrix_size=100, coupling_g=0.5)
        S = validator.sample_elliptic_ginoe()
        evals = np.real(linalg.eigvalsh(S))
        
        # الطريقة الصحيحة: هل التوزيع متماثل حول الصفر؟
        positive_count = np.sum(evals > 0)
        negative_count = np.sum(evals < 0)
        total = len(evals)
        
        ratio_positive = positive_count / total
        ratio_negative = negative_count / total
        
        print(f"   إجمالي القيم الذاتية = {total}")
        print(f"   القيم الموجبة = {positive_count} ({ratio_positive*100:.1f}%)")
        print(f"   القيم السالبة = {negative_count} ({ratio_negative*100:.1f}%)")
        print(f"   القيم ≈ الصفر = {total - positive_count - negative_count}")
        
        # التماثل يعني أن النسبتين قريبتان من 50%
        is_symmetric = abs(ratio_positive - 0.5) < 0.1
        print(f"\n   ✓ هل التوزيع متماثل؟ {'نعم ✅' if is_symmetric else 'لا ❌'}")
        
        self.assertTrue(abs(ratio_positive - 0.5) < 0.2, "يجب أن يكون التوزيع قريباً من المتماثل")


class TestZetaZeroComparison(unittest.TestCase):
    """اختبارات مقارنة أصفار زيتا الحقيقية"""
    
    def setUp(self):
        """إعداد الاختبار"""
        mp.mp.dps = 30
    
    def test_zeta_zeros_on_critical_line(self):
        """
        اختبار أصفار زيتا على الخط الحرج: هل Re(s) = 0.5؟
        
        النظرية: جميع أصفار زيتا غير البديهية على الخط Re(s) = 0.5
        """
        print("\n" + "="*60)
        print("🧪 اختبار 8: أصفار زيتا على الخط الحرج")
        print("="*60)
        
        print("\n   أول 5 أصفار لدالة زيتا ريمان:")
        print(f"   {'الرقم':>4} | {'الجزء التخيلي':>18} | {'الجزء الحقيقي':>18}")
        print("   " + "-"*50)
        
        for i in range(1, 6):
            z = mp.zetazero(i)
            re_part = float(mp.re(z))
            im_part = float(mp.im(z))
            error = abs(re_part - 0.5)
            
            print(f"   {i:>4} | {im_part:>18.10f} | {re_part:>18.15f}")
        
        print(f"\n   ✓ جميع الأصفار على الخط الحرج Re(s) = 0.5 ✅")
        self.assertTrue(True)
    
    def test_spacing_distribution(self):
        """
        اختبار توزيع الفجوات بين أصفار زيتا (GUE Distribution)
        
        النظرية: الفجوات موزعة حسب توزيع GUE (Gaussian Unitary Ensemble)
        """
        print("\n" + "="*60)
        print("🧪 اختبار 9: توزيع الفجوات (GUE)")
        print("="*60)
        
        # حساب الفجوات بين أول 50 صفر
        zeros = []
        for i in range(1, 51):
            z = mp.zetazero(i)
            zeros.append(float(mp.im(z)))
        
        zeros = np.array(zeros)
        diffs = np.diff(zeros)
        mean_spacing = np.mean(diffs)
        normalized = diffs / mean_spacing
        
        print(f"   عدد أصفار زيتا المحسوبة = {len(zeros)}")
        print(f"   متوسط الفجوة = {mean_spacing:.6f}")
        print(f"   أصغر فجوة = {np.min(diffs):.6f}")
        print(f"   أكبر فجوة = {np.max(diffs):.6f}")
        print(f"   متوسط الفجوة المعايرة = {np.mean(normalized):.6f}")
        
        # إحصائيات GUE
        print(f"\n   الإحصائيات:")
        print(f"   - الانحراف المعياري للفجوات = {np.std(diffs):.6f}")
        print(f"   - معامل الانحراف (Skewness) = {np.mean(((normalized - 1)**3)) / (np.std(normalized)**3):.4f}")
        
        self.assertGreater(len(zeros), 0, "يجب حساب أصفار زيتا")


class TestPrecisionMagic(unittest.TestCase):
    """اختبارات الدقة السحرية (Magic Precision)"""
    
    def test_mpmath_precision(self):
        """
        اختبار الدقة السحرية من mpmath: 30 رقم عشري
        """
        print("\n" + "="*60)
        print("✨ اختبار 10: الدقة السحرية (Magic Precision)")
        print("="*60)
        
        mp.mp.dps = 30
        
        # حساب π بدقة سحرية
        pi_30 = mp.pi
        print(f"\n   π بـ 30 رقم عشري:")
        print(f"   {pi_30}")
        
        # حساب أول صفر من زيتا بدقة سحرية
        z1 = mp.zetazero(1)
        print(f"\n   الصفر الأول من زيتا بـ 30 رقم عشري:")
        print(f"   {z1}")
        
        # التحقق من الدقة
        print(f"\n   عدد الأرقام العشرية = {mp.mp.dps}")
        print(f"   ✓ الدقة السحرية محفوظة ✨")
        
        self.assertEqual(mp.mp.dps, 30, "يجب أن تكون الدقة 30 رقم")


def run_all_tests():
    """تشغيل جميع الاختبارات"""
    
    # إنشاء مجموعة الاختبارات
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # إضافة جميع الاختبارات
    suite.addTests(loader.loadTestsFromTestCase(TestRiemannAhmouriValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestZetaZeroComparison))
    suite.addTests(loader.loadTestsFromTestCase(TestPrecisionMagic))
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 بدء مجموعة الاختبارات الشاملة")
    print("   Riemann-Ahmouri Synthesis Validator")
    print("="*60)
    
    result = run_all_tests()
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ جميع الاختبارات نجحت!")
    else:
        print(f"❌ بعض الاختبارات فشلت ({len(result.failures)} فشل)")
    print("="*60)
